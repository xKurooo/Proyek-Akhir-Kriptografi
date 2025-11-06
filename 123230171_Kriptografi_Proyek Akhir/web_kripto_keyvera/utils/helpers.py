# web_kripto_keyvera/utils/helpers.py
import hashlib
from flask import flash
from web_kripto_keyvera.config import Config

def get_key_from_password(password_str):
    """Derivasi kunci dari password menggunakan SHA-256 (32-byte key)."""
    return hashlib.sha256(password_str.encode('utf-8')).digest()

def allowed_file(filename):
    """Validasi ekstensi file untuk enkripsi file."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def allowed_stego_cover_file(filename):
    """Validasi file cover untuk steganografi (jpg/png)."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_STEGO_COVER_EXTENSIONS

def allowed_stego_extract_file(filename):
    """Validasi file stego untuk ekstraksi (harus .png)."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_STEGO_EXTRACT_EXTENSIONS

def validate_adfgx_keys(square_key, transpose_key):
    """Validasi format kunci ADFGX."""
    import re
    square_key_clean = re.sub(r'[^A-Z]', '', square_key.upper().replace('J', 'I'))
    transpose_key_clean = re.sub(r'[^A-Z]', '', transpose_key.upper())
    
    if len(square_key_clean) != 25 or len(set(square_key_clean)) != 25:
        flash('Kunci Square ADFGX harus valid: 25 karakter alfabet unik (I/J digabung).', 'error')
        return None, None
    if not transpose_key_clean:
        flash('Kunci Transpose ADFGX tidak boleh kosong.', 'error')
        return None, None
    
    return square_key_clean, transpose_key_clean
