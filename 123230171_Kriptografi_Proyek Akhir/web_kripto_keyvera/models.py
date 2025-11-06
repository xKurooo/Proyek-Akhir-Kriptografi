# web_kripto_keyvera/models.py
from . import db

class User(db.Model):
    """
    Model tabel pengguna untuk autentikasi.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary(60), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
