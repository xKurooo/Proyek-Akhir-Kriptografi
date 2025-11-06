# web_kripto_keyvera/utils/crypto_utils.py
import os, base64, re
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from pycipher import ADFGX

# === ChaCha20 Text ===
def encrypt_text_chacha20(plaintext, key):
    nonce = os.urandom(12)
    chacha = ChaCha20Poly1305(key)
    ciphertext = chacha.encrypt(nonce, plaintext.encode('utf-8'), None)
    return nonce + ciphertext

def decrypt_text_chacha20(nonce_and_ciphertext, key):
    nonce = nonce_and_ciphertext[:12]
    ciphertext = nonce_and_ciphertext[12:]
    chacha = ChaCha20Poly1305(key)
    try:
        return chacha.decrypt(nonce, ciphertext, None).decode('utf-8')
    except Exception:
        return None

# === ChaCha20 File ===
def encrypt_file_chacha(plaintext_bytes, key):
    nonce = os.urandom(12)
    chacha = ChaCha20Poly1305(key)
    ciphertext = chacha.encrypt(nonce, plaintext_bytes, None)
    return nonce + ciphertext

def decrypt_file_chacha(encrypted_bytes, key):
    try:
        nonce = encrypted_bytes[:12]
        ciphertext = encrypted_bytes[12:]
        chacha = ChaCha20Poly1305(key)
        decrypted_data = chacha.decrypt(nonce, ciphertext, None)
        return decrypted_data
    except Exception as e:
        print(f"Dekripsi file ChaCha20 gagal: {e}")
        return None

# === ADFGX Cipher ===
def encrypt_adfgx(plaintext, key_square, key_transpose):
    try:
        adfgx_cipher = ADFGX(key_square, key_transpose)
        clean_text = plaintext.upper().replace('J', 'I')
        clean_text = re.sub(r'[^A-Z0-9]', '', clean_text)
        if not clean_text:
            return ""
        return adfgx_cipher.encipher(clean_text)
    except Exception:
        return None

def decrypt_adfgx(ciphertext, key_square, key_transpose):
    try:
        adfgx_cipher = ADFGX(key_square, key_transpose)
        clean_cipher = ciphertext.upper()
        clean_cipher = re.sub(r'[^ADFGX]', '', clean_cipher)
        if not clean_cipher:
            return ""
        return adfgx_cipher.decipher(clean_cipher)
    except Exception:
        return None

# === Kombinasi Super Cipher ===
def encrypt_super(plaintext, adfgx_sq, adfgx_tr, password_str, get_key_func, encrypt_text_func):
    key_sq, key_tr = adfgx_sq, adfgx_tr
    intermediate = encrypt_adfgx(plaintext, key_sq, key_tr)
    key_chacha = get_key_func(password_str)
    encrypted_bytes = encrypt_text_func(intermediate, key_chacha)
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def decrypt_super(ciphertext_b64, adfgx_sq, adfgx_tr, password_str, get_key_func, decrypt_text_func):
    try:
        key_sq, key_tr = adfgx_sq, adfgx_tr
        key_chacha = get_key_func(password_str)
        data_to_decrypt = base64.b64decode(ciphertext_b64)
        intermediate = decrypt_text_func(data_to_decrypt, key_chacha)
        if intermediate is None:
            return None
        return decrypt_adfgx(intermediate, key_sq, key_tr)
    except Exception:
        return None
