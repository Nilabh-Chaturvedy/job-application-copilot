import pdfplumber

def extract_text_from_pdf(pdf_path:str)->str:
    text_part=[]

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text=page.extract_text()
            if page_text:
                text_part.append(page_text)
    
    return "\n".join(text_part).strip()

