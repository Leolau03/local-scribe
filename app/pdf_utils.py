import fitz  # PyMuPDF

def fill_pdf(template_path: str, output_path: str, data: dict):
    doc = fitz.open(template_path)
    
    for page in doc:
        for widget in page.widgets():
            # If the PDF field name matches a key in our JSON, fill it
            if widget.field_name in data:
                val = data[widget.field_name]
                widget.field_value = str(val) if val is not None else ""
                widget.update()

    doc.save(output_path)
    doc.close()
    return output_path