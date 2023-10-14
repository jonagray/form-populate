from flask import Flask, request, send_file
from PyPDF2 import PdfFileReader, PdfFileWriter
import io

app = Flask(__name__)

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    # Extract data from form
    name = request.form.get('name')
    email = request.form.get('email')

    # Load PDF Template and get form fields
    pdf_template = PdfFileReader(open('template.pdf', 'rb'))
    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(pdf_template.getPage(0))

    # Populate the PDF
    pdf_writer.updatePageFormFieldValues(pdf_writer.getPage(0), {'name_field': name, 'email_field': email})
    
    # Create response
    output_stream = io.BytesIO()
    pdf_writer.write(output_stream)
    output_stream.seek(0)
    return send_file(output_stream, as_attachment=True, download_name='populated.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(port=5000)
