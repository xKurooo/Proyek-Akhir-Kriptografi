# web_kripto_keyvera/routes/main_routes.py
from flask import Blueprint, render_template, redirect, url_for, session, flash

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def home():
    """Halaman utama: dashboard jika login, landing page jika belum."""
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        return render_template('welcome.html')  # kita buat juga halaman sambutan ringan

@main_bp.route('/register_page')
def register_page():
    return render_template('register.html')

@main_bp.route('/login_page')
def login_page():
    return render_template('login.html')

@main_bp.route('/text_crypto_page')
def text_crypto_page():
    if 'username' not in session:
        flash('Anda harus login untuk mengakses halaman ini.')
        return redirect(url_for('main_bp.login_page'))
    return render_template('text_crypto.html', form_data={})

@main_bp.route('/file_crypto_page')
def file_crypto_page():
    if 'username' not in session:
        flash('Anda harus login untuk mengakses halaman ini.')
        return redirect(url_for('main_bp.login_page'))
    return render_template('file_crypto.html', algorithm_name="ChaCha20-Poly1305")

@main_bp.route('/steganography_page')
def steganography_page():
    if 'username' not in session:
        flash('Anda harus login untuk mengakses halaman ini.')
        return redirect(url_for('main_bp.login_page'))
    return render_template('steganography.html')
