from reportlab.pdfgen import canvas
from io import BytesIO

def generate_certificate(donor_name, amount):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    # Add certificate content
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(200, 750, "Certificate of Appreciation")
    pdf.setFont("Helvetica", 14)
    pdf.drawString(50, 700, f"This is to certify that {donor_name} has generously donated")
    pdf.drawString(50, 680, f"an amount of ₹{amount} to support our cause.")
    pdf.drawString(50, 660, "We deeply appreciate your contribution and support.")
    pdf.drawString(50, 600, "Thank you for making a difference!")

    pdf.setFont("Helvetica-Oblique", 12)
    pdf.drawString(50, 550, "Date: _______________________")
    pdf.drawString(350, 550, "Authorized Signature: _______________________")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer
