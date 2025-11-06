# web_kripto_keyvera/routes/stego_routes.py
from flask import Blueprint, request, redirect, url_for, flash, render_template, session, send_file
import io
from web_kripto_keyvera.utils.helpers import allowed_stego_cover_file, allowed_stego_extract_file
from web_kripto_keyvera.utils.stego_utils import embed_random_lsb, extract_random_lsb

stego_bp = Blueprint('stego_bp', __name__)

@stego_bp.route('/embed_image', methods=['POST'])
def embed_image():
    if 'username' not in session:
        return redirect(url_for('main_bp.login_page'))
    if 'image_file' not in request.files:
        flash('Tidak ada gambar yang di-upload.', 'error')
        return redirect(url_for('main_bp.steganography_page'))
    file = request.files['image_file']
    message = request.form.get('secret_message', '')
    password_str = request.form.get('secret_key', '')

    if file.filename == '':
        flash('Nama file tidak boleh kosong.', 'error')
        return redirect(url_for('main_bp.steganography_page'))
    if not message:
        flash('Pesan rahasia tidak boleh kosong.', 'error')
        return redirect(url_for('main_bp.steganography_page'))
    if not password_str:
        flash('Kunci rahasia tidak boleh kosong.', 'error')
        return redirect(url_for('main_bp.steganography_page'))
    if not allowed_stego_cover_file(file.filename):
        flash('File cover harus .jpg atau .png', 'error')
        return redirect(url_for('main_bp.steganography_page'))

    try:
        stego_bytes = embed_random_lsb(file.read(), message, password_str)
        base_name = file.filename.rsplit('.', 1)[0]
        out_name = f'stego_{base_name}.png'
        return send_file(io.BytesIO(stego_bytes), mimetype='image/png', as_attachment=True, download_name=out_name)
    except Exception as e:
        flash(f'Terjadi error: {e}', 'error')
        return redirect(url_for('main_bp.steganography_page'))

@stego_bp.route('/extract_image', methods=['POST'])
def extract_image():
    if 'username' not in session:
        return redirect(url_for('main_bp.login_page'))
    if 'stego_file' not in request.files:
        flash('Tidak ada gambar yang di-upload.', 'error')
        return redirect(url_for('main_bp.steganography_page'))
    file = request.files['stego_file']
    password_str = request.form.get('secret_key', '')

    if file.filename == '':
        flash('Nama file tidak boleh kosong.', 'error')
        return redirect(url_for('main_bp.steganography_page'))
    if not password_str:
        flash('Kunci rahasia tidak boleh kosong.', 'error')
        return redirect(url_for('main_bp.steganography_page'))
    if not allowed_stego_extract_file(file.filename):
        flash('File stego harus .png', 'error')
        return redirect(url_for('main_bp.steganography_page'))

    try:
        extracted = extract_random_lsb(file.read(), password_str)
        fail = "[EOM tidak ditemukan / Kunci salah / Tidak ada pesan]"
        if extracted == fail:
            flash(fail, 'error')
        else:
            flash('Pesan berhasil diekstrak!', 'success')
        return render_template('steganography.html', extracted_message=extracted)
    except Exception as e:
        flash(f'Terjadi error saat ekstrak: {e}', 'error')
        return redirect(url_for('main_bp.steganography_page'))