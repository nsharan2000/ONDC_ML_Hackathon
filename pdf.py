import PyPDF2

def extract_metadata_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        metadata = pdf_reader.getDocumentInfo()
    return metadata

metadata1 = extract_metadata_from_pdf('Data/2.pdf')
metadata2 = extract_metadata_from_pdf('Data/the_customs_act,_1962.pdf')

# Compare metadata
if metadata1 == metadata2:
    print("Metadata is identical.")
else:
    print("Metadata is different.")
