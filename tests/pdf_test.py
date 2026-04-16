import os

from src.pdf_parser import extract_text_from_pdf


if __name__ == "__main__":
    pdf_path = os.getenv("TEST_RESUME_PDF", "data/resume.pdf")
    text = extract_text_from_pdf(pdf_path)

    print("\n--- EXTRACTED TEXT ---\n")
    print(text[:2000])
