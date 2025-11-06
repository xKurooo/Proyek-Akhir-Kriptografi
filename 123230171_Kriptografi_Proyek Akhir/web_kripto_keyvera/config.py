# web_kripto_keyvera/config.py
import os

class Config:
    # SECRET_KEY: gunakan env var jika ada, kalau tidak buat random saat runtime (untuk dev)
    SECRET_KEY = os.environ.get('WEB_KRIPTO_SECRET') or os.urandom(24)

    # Database: tetap gunakan string yang kamu minta
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/web_kripto'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload / allowed extensions (mirip konstanta di app.py)
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    ALLOWED_STEGO_COVER_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    ALLOWED_STEGO_EXTRACT_EXTENSIONS = {'png'}

    # Other config constants
    EOM_MARKER = "1111111111111110"
