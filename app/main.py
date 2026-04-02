import os
import shutil
from typing import Dict, Any
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import FileResponse, HTMLResponse 
from fastapi.staticfiles import StaticFiles
from transcription import transcribe_audio
from extraction import get_dynamic_schema, extract_structured_data
from pdf_utils import fill_pdf

app = FastAPI()

# Mount a folder for our frontend files
app.mount("/static", StaticFiles(directory="/app/frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serves the main UI."""
    with open("/app/frontend/index.html", "r") as f:
        return f.read()
    
# --- CHECK FOR TEMPLATES ---
@app.get("/formats")
async def list_formats():
    formats_dir = "/app/formats"
    if not os.path.exists(formats_dir):
        return {"formats": []}
    
    # Get all folder names inside the formats directory
    formats = [d for d in os.listdir(formats_dir) if os.path.isdir(os.path.join(formats_dir, d))]
    return {"formats": formats}
    
# --- EXTRACT DATA ---
@app.post("/extract/{format_name}")
async def extract_data(format_name: str, file: UploadFile):
    temp_audio = f"temp_{file.filename}"
    with open(temp_audio, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        print(f"📝 Transcribing {format_name}...")
        transcript = transcribe_audio(temp_audio)

        SchemaClass = get_dynamic_schema(format_name)
        data_object = extract_structured_data(transcript, SchemaClass)
        data_dict = data_object.model_dump()

        # --- 🌟 NEW: Format the lists dynamically based on schema.py ---
        config = getattr(SchemaClass, "LayoutConfig", None)
        if config and hasattr(config, "list_formatting"):
            for list_field, format_string in config.list_formatting.items():
                # If the LLM found data for this list
                if list_field in data_dict and isinstance(data_dict[list_field], list):
                    formatted_items = []
                    for item in data_dict[list_field]:
                        # Replaces {name}, {dose}, etc., with the actual values!
                        formatted_items.append(format_string.format(**item))
                    
                    # Replace the raw list with our beautiful new string
                    data_dict[list_field] = "\n".join(formatted_items)
        # ---------------------------------------------------------------

        return {"message": "Success", "data": data_dict}
    finally:
        if os.path.exists(temp_audio):
            os.remove(temp_audio)

# --- GENERATE PDF ---
@app.post("/generate_pdf/{format_name}")
async def generate_pdf(format_name: str, data: Dict[str, Any]):
    SchemaClass = get_dynamic_schema(format_name)
    config = getattr(SchemaClass, "LayoutConfig", None)
    
    final_pdf_data = data.copy()

    if config and getattr(config, "layout_type", "") == "UNIQUE":
        
        # 1. Map simple text fields to the PDF boxes
        if hasattr(config, "text_mapping"):
            for schema_field, pdf_box in config.text_mapping.items():
                if data.get(schema_field): 
                    final_pdf_data[pdf_box] = data[schema_field]

        # 2. Map the lists of strings to PDF Checkboxes
        if hasattr(config, "checkbox_mapping"):
            for list_field, mapping in config.checkbox_mapping.items():
                if list_field in data:
                    raw_data = data[list_field]
                    selected_options = []
                    
                    # If it came from the frontend text box, it's a string separated by newlines
                    if isinstance(raw_data, str):
                        # Split it back into a list and clean up any extra spaces
                        selected_options = [opt.strip() for opt in raw_data.split('\n') if opt.strip()]
                    # If it came directly from the AI, it's already a list
                    elif isinstance(raw_data, list):
                        selected_options = raw_data

                    # Now loop through the restored list and check the boxes!
                    for selected_option in selected_options:
                        if selected_option in mapping:
                            pdf_checkbox_name = mapping[selected_option]
                            final_pdf_data[pdf_checkbox_name] = "/Yes"

        # 3. The "Other" Combo Move (Auto-check the box if text exists)
        if data.get("other_antecedent_text") and hasattr(config, "other_antecedent_checkbox"):
            final_pdf_data[config.other_antecedent_checkbox] = "/Yes"
            
        if data.get("other_consequence_text") and hasattr(config, "other_consequence_checkbox"):
            final_pdf_data[config.other_consequence_checkbox] = "/Yes"

    elif config and getattr(config, "layout_type", "") == "TABLE_FLATTEN":
        for list_field, pdf_box in config.table_mapping.items():
            if list_field in data:
                
                # If it's a string from the frontend, map it directly
                if isinstance(data[list_field], str):
                    final_pdf_data[pdf_box] = data[list_field]
                    
                    # Optional: Remove the original list_field key if it's different 
                    # from the pdf_box name, to keep the payload clean
                    if list_field != pdf_box:
                         del final_pdf_data[list_field]

                # ... (Scenario B logic remains the same if needed for direct API calls)
                elif isinstance(data[list_field], list):
                    rows = []
                    for item in data[list_field]:
                        row_values = [str(v) for v in item.values()]
                        rows.append(" | ".join(row_values))
                    final_pdf_data[pdf_box] = "\n".join(rows)

    # Add the debug print statement here to verify the payload
    print(f"\n📝 DEBUG PDF PAYLOAD: {final_pdf_data}\n")

    template = f"/app/formats/{format_name}/template.pdf"
    output_path = f"/app/outputs/output_{format_name}.pdf"
    fill_pdf(template, output_path, final_pdf_data)

    return {"download_url": f"/download/output_{format_name}.pdf"}

# --- DOWNLOAD PDF ---
@app.get("/download/{filename}")
async def download_file(filename: str):
    return FileResponse(path=f"/app/outputs/{filename}", filename=filename)

