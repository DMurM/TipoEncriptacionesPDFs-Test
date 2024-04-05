from flask import Flask, request
from flask_cors import CORS
import os
import subprocess
import csv

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_password_in_csv(pdf_hash):
    csv_file = 'passwords.csv'
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            if row[1] == pdf_hash:
                return row[0]  # Retorna la contraseña si el hash coincide
    return None

def save_hash_to_csv(pdf_filename, pdf_hash):
    csv_file = 'passwords.csv'  # Nombre del archivo CSV para almacenar contraseñas y hashes
    if not is_hash_in_csv(pdf_hash):  # Verifica si el hash ya existe en el CSV
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([pdf_filename, pdf_hash])

def is_hash_in_csv(pdf_hash):
    csv_file = 'passwords.csv'
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            if row[1] == pdf_hash:
                return True
    return False

def convert_pdf_to_hash(pdf_path):
    try:
        perl_exe_path = r'C:\Strawberry\perl\bin\perl.exe'  # Ruta al intérprete de Perl
        pdf2john_script = r'C:\john\run\pdf2john.pl'        # Ruta al script pdf2john.pl

        result = subprocess.run([perl_exe_path, pdf2john_script, pdf_path], capture_output=True, text=True)

        if result.returncode == 0:
            pdf_hash = result.stdout.strip()
            save_hash_to_csv(os.path.basename(pdf_path), pdf_hash)  # Guarda el hash en el CSV si no existe
            password = find_password_in_csv(pdf_hash)
            if password:
                return f"Contraseña: {password}\nHash: {pdf_hash}"
            else:
                return f"No se encontró la contraseña para el hash: {pdf_hash}"
        else:
            return None
    except Exception as e:
        print(f"Error al convertir el archivo PDF a hash: {e}")
        return None

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return 'No se ha seleccionado ningún archivo PDF.'
    file = request.files['pdf']
    if file.filename == '':
        return 'Ningún archivo seleccionado.'
    if file and allowed_file(file.filename):
        if not os.path.exists('pdf_files'):
            os.makedirs('pdf_files')
        file_path = os.path.join('pdf_files', file.filename)
        file.save(file_path)

        hash_result = convert_pdf_to_hash(file_path)

        if hash_result:
            return hash_result
        else:
            return 'El archivo PDF no se pudo convertir.'
    else:
        return 'La extensión del archivo no está permitida o el archivo está vacío.'

if __name__ == '__main__':
    app.run(debug=False, port=5500)
