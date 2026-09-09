"""
Generates a PDF bill for an Order and saves it onto order.bill_pdf.
"""
import io
from django.conf import settings
from django.core.files.base import ContentFile
from reportlab.lib import colors
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
)

RED = colors.HexColor('#B3211A')
RED_DARK = colors.HexColor('#7E1712')
GOLD = colors.HexColor('#D9A441')
INK = colors.HexColor('#2A1A15')
INK_SOFT = colors.HexColor('#7A675E')


def generate_order_bill_pdf(order) -> str:
    """Builds the PDF, saves it to order.bill_pdf, and returns the relative path."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A5,
        topMargin=16 * mm, bottomMargin=14 * mm,
        leftMargin=14 * mm, rightMargin=14 * mm,
        title=f"Order #{order.id} - {settings.SHOP_NAME}",
    )

    styles = getSampleStyleSheet()
    shop_style = ParagraphStyle('Shop', parent=styles['Title'], fontSize=20, textColor=RED_DARK, spaceAfter=2, alignment=1)
    tagline_style = ParagraphStyle('Tagline', parent=styles['Normal'], fontSize=9, textColor=INK_SOFT, alignment=1, spaceAfter=10)
    label_style = ParagraphStyle('Label', parent=styles['Normal'], fontSize=10, textColor=INK, spaceAfter=2)
    total_style = ParagraphStyle('Total', parent=styles['Normal'], fontSize=14, textColor=RED_DARK, alignment=2, fontName='Helvetica-Bold')
    breakdown_style = ParagraphStyle('Breakdown', parent=styles['Normal'], fontSize=10, textColor=INK_SOFT, alignment=2, spaceAfter=3)

    elements = []
    elements.append(Paragraph(settings.SHOP_NAME, shop_style))
    elements.append(Paragraph("Order Bill", tagline_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))

    elements.append(Paragraph(f"<b>Order #{order.id}</b> &nbsp;&middot;&nbsp; {order.created_at.strftime('%d %b %Y, %I:%M %p')}", label_style))
    elements.append(Paragraph(f"<b>Customer:</b> {order.customer_name}", label_style))
    elements.append(Paragraph(f"<b>Phone:</b> {order.phone_number}", label_style))
    elements.append(Paragraph(f"<b>Type:</b> {order.get_order_type_display()}", label_style))
    if order.order_type == 'DELIVERY' and order.address:
        elements.append(Paragraph(f"<b>Address:</b> {order.address}", label_style))
    if order.notes:
        elements.append(Paragraph(f"<b>Notes:</b> {order.notes}", label_style))
    elements.append(Spacer(1, 10))

    data = [["Item", "Size", "Qty", "Price", "Subtotal"]]
    for item in order.items.all():
        data.append([
            item.item_name,
            item.get_size_display(),
            str(item.quantity),
            f"Rs. {item.price}",
            f"Rs. {item.subtotal()}",
        ])

    table = Table(data, colWidths=[52 * mm, 18 * mm, 12 * mm, 22 * mm, 24 * mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), RED),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FBF4E7')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2D5C4')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"Items subtotal: Rs. {order.items_subtotal()}", breakdown_style))
    elements.append(Paragraph(f"Service charge: Rs. {order.service_charge}", breakdown_style))
    elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
    elements.append(Paragraph(f"TOTAL: Rs. {order.total_amount}", total_style))
    elements.append(Spacer(1, 16))
    elements.append(Paragraph("Thank you for ordering with us!", tagline_style))

    doc.build(elements)
    buffer.seek(0)

    filename = f"order_{order.id}_bill.pdf"
    order.bill_pdf.save(filename, ContentFile(buffer.read()), save=True)
    return order.bill_pdf.name
