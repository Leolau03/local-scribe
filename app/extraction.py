import os
import importlib.util
from openai import OpenAI
import instructor
from pydantic import BaseModel

# Connect to the Ollama container using the OpenAI compatibility layer
ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")

# We use the OpenAI client, but point it at our local engine
client = instructor.from_openai(
    OpenAI(
        base_url=f"{ollama_host}/v1",
        api_key="ollama" # OpenAI requires a key, but Ollama ignores it
    ),
    mode=instructor.Mode.JSON
)

def get_dynamic_schema(format_name: str):
    """Dynamically loads the Pydantic model 'ReportSchema' from the format folder."""
    path = f"/app/formats/{format_name}/schema.py"
    spec = importlib.util.spec_from_file_location("schema", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ReportSchema

def extract_structured_data(transcript: str, schema_class: type[BaseModel]):
    return client.chat.completions.create(
        model="qwen2.5:7b", # Or whatever model you pulled via your setup.sh
        messages=[{"role": "user", "content": f"Extract info from this text: {transcript}"}],
        response_model=schema_class,
    )