import PyPDF2
import os

directorio_actual = os.path.dirname(__file__)

directorio_pdf = os.path.join(directorio_actual, 'pdf_files')

archivos_pdf = [archivo for archivo in os.listdir(directorio_pdf) if archivo.endswith('.pdf')]

for archivo_pdf in archivos_pdf:
    ruta_pdf = os.path.join(directorio_pdf, archivo_pdf)

    with open(ruta_pdf, 'rb') as archivo_pdf:
        pdf_pass = PyPDF2.PdfFileReader(archivo_pdf)
        print(pdf_pass)
