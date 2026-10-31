"""Builds the GrassCrafts review QR card (90x55 mm, front + back) and an A4 print sheet."""
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Serif-B", F + "DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif", F + "DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("Sans", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-B", F + "DejaVuSans-Bold.ttf"))

GREEN, CREAM, BROWN, GOLD = HexColor("#4F6F33"), HexColor("#F6F0E4"), HexColor("#3E2723"), HexColor("#B8893B")
W, H = 90 * mm, 55 * mm
GOOGLE = "https://search.google.com/local/writereview?placeid=ChIJj8JSa12f-DkRUC8tUXwc-kA"
SITE = "https://grasscrafts.com/pages/review-us"


def qr(c, url, x, y, size):
    w = QrCodeWidget(url, barLevel="M")
    b = w.getBounds()
    d = Drawing(size, size, transform=[size / (b[2] - b[0]), 0, 0, size / (b[3] - b[1]), 0, 0])
    d.add(w)
    c.setFillColor(white)
    c.roundRect(x - 1.2 * mm, y - 1.2 * mm, size + 2.4 * mm, size + 2.4 * mm, 1.5 * mm, stroke=0, fill=1)
    renderPDF.draw(d, c, x, y)


def weave(c, x, y, w, h):
    """Thin woven-stripe border, a nod to madur and sabai weaving."""
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    step = 2.2 * mm
    i = x
    while i < x + w:
        c.line(i, y, i + step / 2, y + h)
        i += step


def front(c, ox, oy):
    c.setFillColor(GREEN)
    c.rect(ox, oy, W, H, stroke=0, fill=1)
    weave(c, ox, oy + H - 3 * mm, W, 3 * mm)
    weave(c, ox, oy, W, 3 * mm)
    c.setFillColor(CREAM)
    c.setFont("Serif-B", 17)
    c.drawCentredString(ox + W / 2, oy + 33 * mm, "GrassCrafts")
    c.setFont("Serif", 6.6)
    c.setFillColor(HexColor("#E8DCC2"))
    c.drawCentredString(ox + W / 2, oy + 28.2 * mm, "by Abalone  ·  handwoven in India since 2015")
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(ox + 30 * mm, oy + 25 * mm, ox + 60 * mm, oy + 25 * mm)
    c.setFillColor(CREAM)
    c.setFont("Sans-B", 8.5)
    c.drawCentredString(ox + W / 2, oy + 18.5 * mm, "Thank you for choosing handmade.")
    c.setFont("Sans", 6.4)
    c.drawCentredString(ox + W / 2, oy + 13.6 * mm, "Every piece is woven by hand from natural grass,")
    c.drawCentredString(ox + W / 2, oy + 10.4 * mm, "cane and fibre by Indian artisans.")
    c.setFont("Sans", 5.6)
    c.setFillColor(HexColor("#E8DCC2"))
    c.drawCentredString(ox + W / 2, oy + 5.2 * mm, "grasscrafts.com")


def back(c, ox, oy):
    c.setFillColor(CREAM)
    c.rect(ox, oy, W, H, stroke=0, fill=1)
    c.setFillColor(GREEN)
    c.rect(ox, oy + H - 11 * mm, W, 11 * mm, stroke=0, fill=1)
    c.setFillColor(CREAM)
    c.setFont("Serif-B", 9.5)
    c.drawCentredString(ox + W / 2, oy + H - 5.6 * mm, "How did we do?")
    c.setFont("Sans", 5.9)
    c.drawCentredString(ox + W / 2, oy + H - 9 * mm, "Your honest review helps other buyers and our artisans.")
    s = 23 * mm
    qy = oy + 12 * mm
    qr(c, GOOGLE, ox + 10 * mm, qy, s)
    qr(c, SITE, ox + W - 10 * mm - s, qy, s)
    c.setFillColor(BROWN)
    c.setFont("Sans-B", 6.6)
    c.drawCentredString(ox + 10 * mm + s / 2, oy + 7.4 * mm, "Review on Google")
    c.drawCentredString(ox + W - 10 * mm - s / 2, oy + 7.4 * mm, "Website & Facebook")
    c.setFont("Sans", 5.4)
    c.setFillColor(GOLD)
    c.drawCentredString(ox + W / 2, oy + 27.5 * mm, "★★★★★")
    c.setFillColor(BROWN)
    c.drawCentredString(ox + W / 2, oy + 23.5 * mm, "Scan with")
    c.drawCentredString(ox + W / 2, oy + 21 * mm, "your phone")
    c.setFont("Sans", 5.3)
    c.drawCentredString(ox + W / 2, oy + 2.6 * mm, "Need help with your order? WhatsApp +91 62907 44782")


def single(path):
    c = canvas.Canvas(path, pagesize=(W, H))
    c.setTitle("GrassCrafts review card")
    front(c, 0, 0); c.showPage()
    back(c, 0, 0); c.showPage()
    c.save()


def sheet(path):
    from reportlab.lib.pagesizes import A4
    pw, ph = A4
    cols, rows = 2, 5
    mx, my = (pw - cols * W) / 2, (ph - rows * H) / 2
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("GrassCrafts review cards - A4 print sheet (10 per page)")
    for side in ("front", "back"):
        for r in range(rows):
            for col in range(cols):
                # mirror columns on the back so the sides line up after flipping on the long edge
                cc = col if side == "front" else cols - 1 - col
                ox, oy = mx + cc * W, my + r * H
                (front if side == "front" else back)(c, ox, oy)
        c.setStrokeColor(HexColor("#999999")); c.setLineWidth(0.25)
        for k in range(cols + 1):
            x = mx + k * W
            c.line(x, my - 4 * mm, x, my - 1 * mm); c.line(x, my + rows * H + 1 * mm, x, my + rows * H + 4 * mm)
        for k in range(rows + 1):
            y = my + k * H
            c.line(mx - 4 * mm, y, mx - 1 * mm, y); c.line(mx + cols * W + 1 * mm, y, mx + cols * W + 4 * mm, y)
        c.showPage()
    c.save()


if __name__ == "__main__":
    single("GrassCrafts_review_card_90x55mm.pdf")
    sheet("GrassCrafts_review_cards_A4_print_sheet.pdf")
    print("done")
