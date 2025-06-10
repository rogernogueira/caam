import os

def list_pdf_files(directory):
    pdf_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_files.append(filename)
    return pdf_files

directory = 'C:\Users\Public'
pdf_files = list_pdf_files(directory)
print(pdf_files)