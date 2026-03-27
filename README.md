# Local Scribe

> A privacy-first, fully local AI pipeline that transforms dictated audio into structured, fillable PDF documents.

Local Scribe leverages local AI models (Whisper for audio transcription and Ollama for structured data extraction) to ensure that no sensitive information ever leaves your machine. It features a built-in "Human-in-the-Loop" Web UI, allowing users to review and edit the AI's extracted notes before automatically stamping them into a final PDF.

---

## ✨ Features

* **100% Local & Private:** Runs entirely on your hardware using Docker, Whisper, and Ollama. No API keys or cloud services required.
* **Human-in-the-Loop:** A dynamic Web UI pauses the pipeline, allowing you to review, correct, and append to the AI's extracted data before the PDF is generated.
* **Dynamic Template Engine:** Add new document types (Invoices, Intake Forms) simply by dropping a PDF and a Pydantic schema into a folder. The UI updates automatically.
* **Multi-Stage Docker Build:** Optimized, lightweight containerization ensuring seamless Mac/Linux/Windows compatibility.

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed on your host machine:
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine + Docker Compose)
* [uv](https://github.com/astral-sh/uv) (Optional, for local Python dependency management)

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/local-scribe.git](https://github.com/yourusername/local-scribe.git)
   cd local-scribe

2. **Run the setup script (if applicable):**
This script pulls the necessary local LLM models (e.g., Qwen, Llama, or DeepSeek) via Ollama.
    ```bash
    chmod +x setup.sh
    ./setup.sh

3. **Access the application:**
Open your web browser and navigate to: http://localhost:8000

---

## 💻 Usage

1. Open the Web UI at ```http://localhost:8000```.
2. Select your desired Document Format from the dropdown menu (e.g., Medical, Invoice).
3. Upload an Audio Recording (.mp3, .wav, .m4a, etc.).
4. Click **1. Transcribe & Extract.** The AI will process the audio and generate editable text boxes based on the document's schema.
5. Review and edit the extracted information for accuracy.
6. Click **2. Generate PDF.** Your finalized PDF will automatically download to your machine!

---

## 📂 Project Structure

```
local-scribe/
├── app/
│   ├── frontend/
│   │   └── index.html       # Vanilla JS/Tailwind Web UI
│   ├── main.py              # FastAPI application and routing
│   ├── extraction.py        # Instructor/Ollama structured data logic
│   ├── transcription.py     # Whisper audio-to-text processing
│   ├── pdf_utils.py         # PDF mapping and generation
│   └── Dockerfile           # Multi-stage Docker build instructions
├── formats/                 # ⭐️ Custom templates live here
│   └── medical/
│       ├── schema.py        # Pydantic schema defining the extraction fields
│       └── template.pdf     # The blank, fillable PDF template
├── outputs/                 # Temporary storage for generated PDFs
├── docker-compose.yml       # Orchestrates the web app and Ollama containers
├── pyproject.toml           # Python dependency configuration (uv)
└── .dockerignore            # Excludes local environments from the Docker context
```
---

## 🛠️ Adding Custom Templates

Local Scribe is designed to be highly modular. You can add new document formats without altering the core Python backend. The Web UI will automatically detect new formats and update the dropdown list.

To add a new format (e.g., an invoice), follow these three steps:

1. **Create a Format Directory**
Create a new folder inside the formats/ directory. The folder name will be used as the format name in the Web UI.
```bash
mkdir formats/invoice
```
2. **Add the Fillable PDF**
Place your fillable PDF into the new folder and name it exactly **template.pdf.**
- Requirement: The PDF must contain interactive form fields. Note the exact names of these fields (e.g., client_name, total_amount).

3. **Create the Extraction Schema**
Create a file named schema.py in the same folder. This file instructs the LLM on what data to extract from the audio.

⚠️ **Crucial Formatting Rule:** The variable names in your Pydantic model must exactly match the interactive form field names inside your template.pdf.

Example: ``formats/invoice/schema.py``

```python
from pydantic import BaseModel, Field

class ReportSchema(BaseModel):
    client_name: str = Field(description="The first and last name of the client")
    service_provided: str = Field(description="A brief description of the work performed")
    total_amount: str = Field(description="The total cost in dollars. Include the $ sign.")
```

Once saved, simply refresh your browser. "Invoice" will now be available in the dropdown!

---

## 🐛 Troubleshooting

- ```ImportError: cannot import name ...```
Ensure your ```pyproject.toml``` dependencies are up to date and re-run ```uv lock```. Rebuild the Docker container using ```docker compose up --build```.

- Changes to ```main.py``` aren't showing up:
Docker caches code. To force a refresh, run:
```docker compose down && docker compose up --build```

- PDF fields are not filling correctly:
Open your template.pdf in a PDF editor and verify the exact names of the form fields. They must match the variables in your ```schema.py``` character-for-character.

- Mac/Linux Executable Errors (exec format error):
Ensure your ```.dockerignore``` file contains ```.venv/ ```and ```app/.venv/``` to prevent your host machine's binaries from bleeding into the Linux container.