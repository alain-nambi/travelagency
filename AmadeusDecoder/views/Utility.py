from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import A4
from django.http import FileResponse
from reportlab.pdfgen import canvas
from io import BytesIO

def create_pdf():
    # Create a BytesIO object to store the PDF content
    pdf_buffer = BytesIO()

    w, h = A4
    pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
    pdf.drawString(50, h - 50, "Hello, world!")
    pdf.showPage()
    
    data = [['Name', 'Age', 'Country'],
    ['John Doe', 30, 'USA'],
    ['Jane Smith', 25, 'Canada'],
    ['Bob Johnson', 35, 'UK']]

    # Create a table and style
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)])


    # Build the PDF document
    table = Table(data, style=style, colWidths=[100, 50, 100])
    table.wrapOn(pdf, 400, 600)  # Adjust the dimensions as needed
    table.drawOn(pdf, 50, 50)
    
    pdf.save()

    # Reset the BytesIO buffer's position to the beginning
    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()

def call_pdf(request):
    pdf_content = create_pdf()

    response = FileResponse(BytesIO(pdf_content), as_attachment=True, filename="example.pdf")
    return response
