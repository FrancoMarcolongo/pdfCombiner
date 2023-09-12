import os
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

gc = gspread.service_account(filename='d:/LeCoq/programming_projects/nrofacreader-dffdcbec5c76.json')

gDocName = "Fravega"
sheet = gc.open(gDocName)

searchParams = sheet.get_worksheet(5).get('L2:L')

searchDir = 'd:\LeCoq\Trabajo\Facturas Fravega'

outputDir = 'd:\Descargas'

def searchPdfs():
    pdfFiles = []
    notFound = searchParams.copy() 
    
    for root, _, files in os.walk(searchDir):
        for filename in files:
            if filename.endswith('.pdf'):
                for param in searchParams:
                    if str(param[0]) in filename and param[0] is not None:
                        pdfFiles.append(os.path.join(root, filename))
                        notFound.remove(param)

    return pdfFiles, notFound

def combinePdfs(archivos_pdf, output_file):
    pdf_writer = PdfWriter()

    for pdf_file in archivos_pdf:
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

    with open(output_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

today = datetime.now().strftime('%d-%m-%y')

combinedPdf = os.path.join(outputDir, f'Facturas Fravega {today}.pdf')

pdfsFound, pdfsNotFound = searchPdfs()

if pdfsFound:
    combinePdfs(pdfsFound, combinedPdf)
    print(f'Se han combinado {len(pdfsFound)} archivos.')
else:
    print('No se encontraron archivos PDF con los números especificados.')

if pdfsNotFound:
    print(f'Archivos no encontrados para los siguientes números: {pdfsNotFound}')
