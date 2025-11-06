# web_kripto_keyvera/utils/stego_utils.py
import io, random, hashlib
from PIL import Image
from web_kripto_keyvera.config import Config

EOM_MARKER = Config.EOM_MARKER

def text_to_bits(text):
    """Konversi teks menjadi bit string dengan EOM marker."""
    bits = ''.join(format(ord(i), '08b') for i in text)
    return bits + EOM_MARKER

def bits_to_text(bits):
    """Konversi bit string kembali ke teks."""
    if bits.endswith(EOM_MARKER):
        bits = bits[:-len(EOM_MARKER)]
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return "".join(chars)

def get_pixel_locations(width, height, password_str):
    """Hasilkan urutan piksel acak berdasarkan hash password."""
    seed = int.from_bytes(hashlib.sha256(password_str.encode('utf-8')).digest()[:4], 'little')
    random.seed(seed)
    locations = [(x, y, c) for y in range(height) for x in range(width) for c in range(3)]
    random.shuffle(locations)
    return locations

def embed_random_lsb(image_bytes, secret_message, password_str):
    """Sembunyikan pesan menggunakan LSB teracak berbasis password."""
    pil_image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    pixels = pil_image.load()
    width, height = pil_image.size
    locations = get_pixel_locations(width, height, password_str)
    secret_bits = text_to_bits(secret_message)
    max_capacity = len(locations)

    if len(secret_bits) > max_capacity:
        raise ValueError("Pesan terlalu panjang untuk kapasitas gambar ini.")

    for i in range(len(secret_bits)):
        x, y, c = locations[i]
        val_list = list(pixels[x, y])
        bit = secret_bits[i]
        val_list[c] = (val_list[c] & ~1) | int(bit)
        pixels[x, y] = tuple(val_list)

    byte_arr = io.BytesIO()
    pil_image.save(byte_arr, format='PNG')
    return byte_arr.getvalue()

def extract_random_lsb(image_bytes, password_str):
    """Ekstrak pesan dari gambar menggunakan urutan LSB teracak."""
    pil_image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    pixels = pil_image.load()
    width, height = pil_image.size
    locations = get_pixel_locations(width, height, password_str)
    extracted_bits = ""

    for (x, y, c) in locations:
        val = pixels[x, y][c]
        extracted_bits += '1' if (val & 1) else '0'
        if extracted_bits.endswith(EOM_MARKER):
            return bits_to_text(extracted_bits)
    return "[EOM tidak ditemukan / Kunci salah / Tidak ada pesan]"