from flask import Flask, render_template, request, send_file, redirect, url_for, session
import qrcode
from io import BytesIO
import re
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  

def is_url(data):
    return re.match(r'^https?://', data) is not None

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_img_data = None
    qr_url = None

    if request.method == 'POST':
        data = request.form['data']
        if data:
            session['qr_data'] = data
            qr_img_data = True
            qr_url = data if is_url(data) else None

    return render_template('index.html', qr_img_data=qr_img_data, qr_url=qr_url)

@app.route('/qr_image')
def qr_image():
    data = session.get('qr_data')
    if not data:
        return redirect(url_for('index'))

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')

@app.route('/download')
def download_qr():
    data = session.get('qr_data')
    if not data:
        return redirect(url_for('index'))

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name='qr_code.png')

if __name__ == '__main__':
    app.run(debug=True)
