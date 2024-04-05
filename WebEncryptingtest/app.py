from flask import Flask, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return 'No se ha seleccionado ningún archivo PDF.'
    file = request.files['pdf']
    if file.filename == '':
        return 'Ningún archivo seleccionado.'
    if file and allowed_file(file.filename):
        if not os.path.exists('WebEncryptingtest/pdf_files'): #Substituir los 3 directorios para enviar los pdfs en "x" directorio
            os.makedirs('WebEncryptingtest/pdf_files') #
        file.save(os.path.join('WebEncryptingtest/pdf_files', file.filename)) #
        return 'Archivo PDF subido exitosamente.'
    else:
        return 'La extensión del archivo no está permitida o el archivo está vacío.'

if __name__ == '__main__':
    app.run(debug=True, port=5500)
