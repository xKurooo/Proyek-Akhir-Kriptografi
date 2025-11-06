# web_kripto_keyvera/routes/crypto_routes.py
from flask import Blueprint, request, render_template, redirect, url_for, flash, session, send_file
import base64, io

from web_kripto_keyvera.utils.helpers import (
    get_key_from_password,
    validate_adfgx_keys,
    allowed_file
)
from web_kripto_keyvera.utils.crypto_utils import (
    encrypt_text_chacha20, decrypt_text_chacha20,
    encrypt_file_chacha, decrypt_file_chacha,
    encrypt_adfgx, decrypt_adfgx,
    encrypt_super, decrypt_super
)

crypto_bp = Blueprint('crypto_bp', __name__)

# === TEXT - ChaCha20 ===
@crypto_bp.route('/encrypt_chacha', methods=['POST'])
def encrypt_chacha():
    if 'username' not in session:
        return redirect(url_for('main_bp.login_page'))
    text_data = request.form.get('text_data', '')
    password_str = request.form.get('secret_key', '')
    form_data = {"text_data_chacha_enc": text_data}

    if not text_data:
        flash('Teks tidak boleh kosong!', 'error')
    elif not password_str:
        flash('Kunci Rahasia diperlukan!', 'error')
    else:
        key = get_key_from_password(password_str)
        encrypted_data = encrypt_text_chacha20(text_data, key)
        result = base64.b64encode(encrypted_data).decode('utf-8')
        flash('ChaCha20 Berhasil Dienkripsi!', 'success')
        return render_template('text_crypto.html', chacha_encrypt_result=result, active_tab='chacha', form_data=form_data)
    return render_template('text_crypto.html', active_tab='chacha', form_data=form_data)

@crypto_bp.route('/decrypt_chacha', methods=['POST'])
def decrypt_chacha():
    if 'username' not in session:
        return redirect(url_for('main_bp.login_page'))
    text_data = request.form.get('text_data', '')
    password_str = request.form.get('secret_key', '')
    form_data = {"text_data_chacha_dec": text_data}
    result = "ERROR: GAGAL DEKRIPSI"
    try:
        if not text_data:
            flash('Ciphertext tidak boleh kosong!', 'error')
        elif not password_str:
            flash('Kunci Rahasia diperlukan!', 'error')
        else:
            key = get_key_from_password(password_str)
            decrypted = decrypt_text_chacha20(base64.b64decode(text_data), key)
            if decrypted is not None:
                result = decrypted
                flash('ChaCha20 Berhasil Didekripsi!', 'success')
            else:
                flash('Dekripsi ChaCha20 Gagal! Kunci atau data salah.', 'error')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return render_template('text_crypto.html', chacha_decrypt_result=result, active_tab='chacha', form_data=form_data)

# === TEXT - ADFGX ===
@crypto_bp.route('/encrypt_adfgx', methods=['POST'])
def encrypt_adfgx_route():
    if 'username' not in session:
        return redirect(url_for('main_bp.login_page'))
    text_data = request.form.get('text_data', '')
    sq = request.form.get('adfgx_square', '')
    tr = request.form.get('adfgx_transpose', '')
    form_data = {"text_data_adfgx_enc": text_data, "adfgx_square_enc": sq, "adfgx_transpose_enc": tr}
    if not text_data:
        flash('Teks tidak boleh kosong!', 'error')
    else:
        key_sq, key_tr = validate_adfgx_keys(sq, tr)
        if key_sq:
            result = encrypt_adfgx(text_data, key_sq, key_tr)
            flash('ADFGX Berhasil Dienkripsi!', 'success')
            return render_template('text_crypto.html', adfgx_encrypt_result=result, active_tab='adfgx', form_data=form_data)
    return render_template('text_crypto.html', active_tab='adfgx', form_data=form_data)

@crypto_bp.route('/decrypt_adfgx', methods=['POST'])
def decrypt_adfgx_route():
    if 'username' not in session:
        return redirect(url_for('main_bp.login_page'))
    text_data = request.form.get('text_data', '')
    sq = request.form.get('adfgx_square', '')
    tr = request.form.get('adfgx_transpose', '')
    form_data = {"text_data_adfgx_dec": text_data, "adfgx_square_dec": sq, "adfgx_transpose_dec": tr}
    result = "ERROR: GAGAL DEKRIPSI"
    if not text_data:
        flash('Ciphertext tidak boleh kosong!', 'error')
    else:
        key_sq, key_tr = validate_adfgx_keys(sq, tr)
        if key_sq:
            decrypted = decrypt_adfgx(text_data, key_sq, key_tr)
            if decrypted is not None:
                result = decrypted
                flash('ADFGX Berhasil Didekripsi!', 'success')
            else:
                flash('Dekripsi ADFGX Gagal! Kunci atau data salah.', 'error')
    return render_template('text_crypto.html', adfgx_decrypt_result=result, active_tab='adfgx', form_data=form_data)

# === TEXT - SUPER CIPHER (ADFGX + ChaCha20) ===
@crypto_bp.route('/encrypt_super', methods=['POST'])
def encrypt_super_route():
    if 'username' not in session:
        return redirect(url_for('main_bp.login_page'))
    text = request.form.get('text_data', '')
    pw = request.form.get('secret_key', '')
    sq = request.form.get('adfgx_square', '')
    tr = request.form.get('adfgx_transpose', '')
    form_data = {"text_data_super_enc": text, "adfgx_square_super_enc": sq, "adfgx_transpose_super_enc": tr}

    if not text:
        flash('Teks tidak boleh kosong!', 'error')
    elif not pw:
        flash('Kunci Rahasia ChaCha20 diperlukan!', 'error')
    else:
        key_sq, key_tr = validate_adfgx_keys(sq, tr)
        if key_sq:
            result = encrypt_super(text, key_sq, key_tr, pw, get_key_from_password, encrypt_text_chacha20)
            flash('Algoritma Super Berhasil Dienkripsi!', 'success')
            return render_template('text_crypto.html', super_encrypt_result=result, active_tab='super', form_data=form_data)
    return render_template('text_crypto.html', active_tab='super', form_data=form_data)

@crypto_bp.route('/decrypt_super', methods=['POST'])
def decrypt_super_route():
    if 'username' not in session:
        return redirect(url_for('main_bp.login_page'))
    text = request.form.get('text_data', '')
    pw = request.form.get('secret_key', '')
    sq = request.form.get('adfgx_square', '')
    tr = request.form.get('adfgx_transpose', '')
    form_data = {"text_data_super_dec": text, "adfgx_square_super_dec": sq, "adfgx_transpose_super_dec": tr}
    result = "ERROR: GAGAL DEKRIPSI"

    if not text:
        flash('Ciphertext tidak boleh kosong!', 'error')
    elif not pw:
        flash('Kunci Rahasia ChaCha20 diperlukan!', 'error')
    else:
        key_sq, key_tr = validate_adfgx_keys(sq, tr)
        if key_sq:
            decrypted = decrypt_super(text, key_sq, key_tr, pw, get_key_from_password, decrypt_text_chacha20)
            if decrypted is not None:
                result = decrypted
                flash('Algoritma Super Berhasil Didekripsi!', 'success')
            else:
                flash('Dekripsi Super Gagal! Kunci atau data salah.', 'error')
    return render_template('text_crypto.html', super_decrypt_result=result, active_tab='super', form_data=form_data)

# === FILE ENCRYPT/DECRYPT ===
@crypto_bp.route('/process_file', methods=['POST'])
def process_file():
    if 'username' not in session:
        return redirect(url_for('main_bp.login_page'))
    if 'file_data' not in request.files:
        flash('Tidak ada file yang di-upload.', 'error')
        return redirect(url_for('main_bp.file_crypto_page'))
    file = request.files['file_data']
    pw = request.form.get('secret_key', '')
    action = request.form['action']

    if file.filename == '':
        flash('Nama file tidak boleh kosong.', 'error')
        return redirect(url_for('main_bp.file_crypto_page'))
    if not pw:
        flash('Kunci rahasia tidak boleh kosong.', 'error')
        return redirect(url_for('main_bp.file_crypto_page'))
    if action == 'encrypt' and not allowed_file(file.filename):
        flash('Tipe file tidak diizinkan!', 'error')
        return redirect(url_for('main_bp.file_crypto_page'))

    try:
        key = get_key_from_password(pw)
        data = file.read()
        if action == 'encrypt':
            processed = encrypt_file_chacha(data, key)
            out_name = file.filename + ".enc"
        else:
            processed = decrypt_file_chacha(data, key)
            if processed is None:
                flash('Dekripsi gagal! Kunci salah.', 'error')
                return redirect(url_for('main_bp.file_crypto_page'))
            out_name = file.filename[:-4] if file.filename.endswith(".enc") else "decrypted_" + file.filename
        return send_file(io.BytesIO(processed), mimetype='application/octet-stream', as_attachment=True, download_name=out_name)
    except Exception as e:
        flash(f'Terjadi error: {e}', 'error')
        return redirect(url_for('main_bp.file_crypto_page'))
