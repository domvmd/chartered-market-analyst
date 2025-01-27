# utils/report_generator.py
from fpdf import FPDF
import tempfile
import streamlit as st

def generate_pdf_report(prediction, analysis):
    """Generate a PDF report with the analysis results"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Function to sanitize text for PDF
    def sanitize_text(text):
        # Replace unsupported Unicode characters with ASCII equivalents
        replacements = {
            "–": "-",  # Replace en dash with hyphen
            "—": "-",  # Replace em dash with hyphen
            "“": '"',  # Replace left double quotation mark with ASCII quote
            "”": '"',  # Replace right double quotation mark with ASCII quote
            "‘": "'",  # Replace left single quotation mark with ASCII quote
            "’": "'",  # Replace right single quotation mark with ASCII quote
            "≈": "≈",  # Approximately equal
            "≠": "!=",  # Not equal
            "≤": "<=",  # Less than or equal
            "≥": ">=",  # Greater than or equal
            "±": "+/-",  # Plus-minus
            "°": "deg",  # Degree symbol
            "•": "*",  # Bullet point
            "…": "...",  # Ellipsis
            "→": "->",  # Right arrow
            "←": "<-",  # Left arrow
            "×": "x",  # Multiplication sign
            "÷": "/",  # Division sign
            "∞": "inf",  # Infinity
            "µ": "u",  # Micro symbol
            "€": "EUR",  # Euro symbol
            "£": "GBP",  # Pound symbol
            "¥": "JPY",  # Yen symbol
            "©": "(c)",  # Copyright
            "®": "(R)",  # Registered trademark
            "™": "(TM)",  # Trademark
            "§": "Sect.",  # Section symbol
            "¶": "P.",  # Paragraph symbol
        }
        # First try to encode as latin-1
        try:
            return text.encode("latin-1", "replace").decode("latin-1")
        except:
            # If that fails, replace remaining special characters
            for old, new in replacements.items():
                text = text.replace(old, new)
            return text.encode("ascii", "replace").decode("ascii")

    # Add title
    pdf.cell(200, 10, txt=sanitize_text("Stock Analysis Report"), ln=True, align="C")

    # Add prediction details
    pdf.cell(200, 10, txt=sanitize_text(f"Ticker: {prediction['ticker']}"), ln=True)
    pdf.cell(
        200,
        10,
        txt=sanitize_text(f"Current Price: ${prediction['last_close']:.2f}"),
