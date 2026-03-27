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

        Schema = get_dynamic_schema(format_name)
        data_object = extract_structured_data(transcript, Schema)
        data_dict = data_object.model_dump()

        return {"message": "Success", "data": data_dict}
    finally:
        if os.path.exists(temp_audio):
            os.remove(temp_audio)

# --- GENERATE PDF ---
@app.post("/generate_pdf/{format_name}")
async def generate_pdf(format_name: str, data: Dict[str, Any]):
    template = f"/app/formats/{format_name}/template.pdf"
    output_name = f"output_{format_name}.pdf"
    output_path = f"/app/outputs/{output_name}"
    
    fill_pdf(template, output_path, data)

    return {
        "message": "PDF Generated",
        "download_url": f"/download/{output_name}"
    }

# --- DOWNLOAD PDF ---
@app.get("/download/{filename}")
async def download_file(filename: str):
    return FileResponse(path=f"/app/outputs/{filename}", filename=filename)

