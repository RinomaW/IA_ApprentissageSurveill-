from flask import render_template, request, redirect, url_for, send_from_directory
import os

UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limite à 16MB

# Assurez-vous que le dossier de téléchargement existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def image_page():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(url_for('image'))

        file = request.files['image']
        if file.filename == '':
            return redirect(url_for('image'))

        if file:
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            image_url = url_for('uploaded_file', filename=file.filename)
            return render_template('TD1templates/image.html', image_url=image_url)

    return render_template('TD1templates/image.html')

UPLOAD_FOLDER = 'C:/Users/romwe/Documents/My Web Sites/IA_FlaskPython/R5.A.05/TD/tp3/uploads'

def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

