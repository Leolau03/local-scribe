import fitz  # PyMuPDF

def fill_pdf(template_path: str, output_path: str, data: dict):
    doc = fitz.open(template_path)
    
    for page in doc:
        # widgets() iterates through all form fields (inputs, checkboxes, etc.)
        for widget in page.widgets():
            field_name = widget.field_name
            
            if field_name in data:
                val = data[field_name]
                
                # 🌟 SPECIAL HANDLING FOR CHECKBOXES
                # In PyMuPDF, widget.field_type 2 is a Checkbox
                if widget.field_type == 2:
                    # If our payload says "/Yes", check the box
                    if val == "/Yes":
                        widget.field_value = True  # Or 1
                    else:
                        widget.field_value = False # Or 0
                else:
                    # Standard text field handling
                    widget.field_value = str(val) if val is not None else ""
                
                # This forces the PDF to redraw the visual element
                widget.update()

    # Save with 'incremental=False' to ensure form data is flattened/saved properly
    doc.save(output_path)
    doc.close()
    return output_path