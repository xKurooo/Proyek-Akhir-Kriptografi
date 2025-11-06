# web_kripto_keyvera/routes/auth_routes.py
from flask import Blueprint, request, redirect, url_for, flash, session
import bcrypt
from web_kripto_keyvera import db
from web_kripto_keyvera.models import User

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Username sudah ada!')
        return redirect(url_for('main_bp.register_page'))

    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash('Akun berhasil dibuat! Silakan login.')
    return redirect(url_for('main_bp.login_page'))

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.checkpw(password, user.password_hash):
        session['username'] = user.username
        flash('Login berhasil!')
        return redirect(url_for('main_bp.home'))
    flash('Username atau Password salah!')
    return redirect(url_for('main_bp.login_page'))

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Anda telah logout.')
    return redirect(url_for('main_bp.home'))