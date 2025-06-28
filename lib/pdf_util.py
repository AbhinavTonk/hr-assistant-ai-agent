from pypdf import PdfReader, PdfWriter, PdfMerger
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def merge_pdfs(pdf_list, output_path):
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

def split_pdf(input_pdf, output_folder):
    reader = PdfReader(input_pdf)
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        with open(f"{output_folder}/page_{i + 1}.pdf", "wb") as f:
            writer.write(f)

# def create_pdf(output_path, text_lines):
#     c = canvas.Canvas(output_path)
#     y = 800
#     for line in text_lines:
#         c.drawString(100, y, line)
#         y -= 20
#     c.save()

def create_pdf(output_path, text):
    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    story = [Paragraph(line, styles["Normal"]) for line in text.split('\n')]
    doc.build(story)