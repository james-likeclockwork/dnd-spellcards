import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register the Cormorant Garamond font
pdfmetrics.registerFont(TTFont('CormorantGaramond', 'fonts/CormorantGaramond-Medium.ttf'))
pdfmetrics.registerFont(TTFont('CormorantGaramond-Italic', 'fonts/CormorantGaramond-MediumItalic.ttf'))
pdfmetrics.registerFont(TTFont('CormorantGaramond-Bold', 'fonts/CormorantGaramond-Bold.ttf'))


# Constants
PAGE_WIDTH, PAGE_HEIGHT = A4
CARD_WIDTH = PAGE_WIDTH / 3
CARD_HEIGHT = PAGE_HEIGHT / 3
MARGIN = 0.1 * inch

# Define styles for the spell card text
title_style = ParagraphStyle(
    "Title",
    fontName="CormorantGaramond-Bold",
    fontSize=12,
    leading=14,
    textColor=colors.black,
    alignment=0,  # left alignment
)

details_style = ParagraphStyle(
    "Details",
    fontName="CormorantGaramond-Italic",
    fontSize=8,
    leading=10,
    textColor=colors.black,
    alignment=0,  # left alignment
)

description_style = ParagraphStyle(
    "Description",
    fontName="CormorantGaramond",
    fontSize=8,
    leading=10,
    textColor=colors.black,
    alignment=0,  # left alignment
)

def draw_card(c, x, y, spell):
    """
    Draws an individual spell card with wrapped text and ensures both details and description fit within the rectangle below the title.
    c : canvas.Canvas object
    x, y : coordinates of the card's top-left corner
    spell : dictionary containing spell details
    """
    # Draw card border (no fill color)
    c.setStrokeColor(colors.black)
    c.rect(x, y, CARD_WIDTH - 2 * MARGIN, CARD_HEIGHT - 2 * MARGIN, fill=0)

    # Title (ensure wrapping)
    title = Paragraph("<u>" + spell["name"] + "</u>", title_style)
    title.wrapOn(c, CARD_WIDTH - 2 * MARGIN, CARD_HEIGHT)
    title.drawOn(c, x + MARGIN, y + CARD_HEIGHT - MARGIN - 20)  # Adjusted y for more spacing

    # Calculate the available height for details and description after the title
    available_height = CARD_HEIGHT - 60  # Card height minus some margin and title space
    details_height = available_height * 0.09
    description_height = available_height * 0.6  # Allocate 60% of the space for description

    # Details (ensure proper wrapping and spacing)
    details = f"Level {spell['level']} {spell['school']}<br/>" \
              f"Casting Time: {spell['casting_time']}<br/>" \
              f"Range: {spell['range']}<br/>" \
              f"Components: {spell['components']}<br/>" \
              f"Duration: {spell['duration']}"
    details_paragraph = Paragraph(details, details_style)
    details_paragraph.wrapOn(c, CARD_WIDTH - 4 * MARGIN, details_height)
    details_paragraph.drawOn(c, x + MARGIN, y + CARD_HEIGHT - MARGIN - 50 - details_height)

    # Adjust the description starting position based on details height
    description_y = y + CARD_HEIGHT - MARGIN - 60 - available_height * 0.87 - 10

    # Ensure the description fits within the remaining space
    description_text = spell["description"]

    # Create the description paragraph
    description_paragraph = Paragraph(description_text, description_style)
    description_paragraph.wrapOn(c, CARD_WIDTH - 4 * MARGIN, description_height + 20)

    # Truncate the description text if it's too long
    description_text = spell["description"]
    description_paragraph = Paragraph(description_text, description_style)
    description_paragraph.wrapOn(c, CARD_WIDTH - 4 * MARGIN, description_height + 20)

    # Draw description
    description_paragraph.drawOn(c, x + MARGIN, description_y)

def generate_spell_cards(data, output_filename="spell_cards.pdf"):
    """
    Generates a PDF with spell cards.
    data : list of dictionaries containing spell details
    output_filename : output filename for the PDF
    """
    c = canvas.Canvas(output_filename, pagesize=A4)

    # Track position of each card
    for i, spell in enumerate(data):
        col = i % 3
        row = (i // 3) % 3
        x = col * CARD_WIDTH + MARGIN
        y = PAGE_HEIGHT - (row + 1) * CARD_HEIGHT + MARGIN

        draw_card(c, x, y, spell)

        # If we’ve filled a page, add a new one
        if (i + 1) % 9 == 0:
            c.showPage()

    # Complete the PDF
    c.save()

# Load spells from JSON file and create the PDF
if __name__ == "__main__":
    # with open("spells.json") as f:
    #     spells_data = json.load(f)
    # generate_spell_cards(spells_data)
    
    with open("spells-elaria.json") as f:
        spells_data = json.load(f)
    generate_spell_cards(spells_data, "Elaria's Spells.pdf")
    
    with open("spells-myra.json") as f:
        spells_data = json.load(f)
    generate_spell_cards(spells_data, "Myra's Spells.pdf")
    
    with open("spells-rendal.json") as f:
        spells_data = json.load(f)
    generate_spell_cards(spells_data, "Rendal's Spells.pdf")
