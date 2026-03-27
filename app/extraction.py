import os
import importlib.util
from openai import OpenAI
import instructor
from pydantic import BaseModel

ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")

client = instructor.from_openai(
    OpenAI(
        base_url=f"{ollama_host}/v1",
        api_key="ollama" 
    ),
    mode=instructor.Mode.JSON
)

def get_dynamic_schema(format_name: str):
    path = f"/app/formats/{format_name}/schema.py"
    spec = importlib.util.spec_from_file_location("schema", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ReportSchema

def get_system_prompt() -> str:
    """Reads the global system prompt from the app directory."""
    path = "/app/system_prompt.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "You are an expert data extraction assistant. Be highly accurate."

# Removed the 'format_name' argument since we don't need it for the prompt anymore!
def extract_structured_data(transcript: str, schema_class: type[BaseModel]):
    system_prompt = get_system_prompt()
    
    return client.chat.completions.create(
        model="qwen2.5:7b",
        temperature=0.0, # Keeps the LLM perfectly factual
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Extract info from this text: {transcript}"}
        ],
        response_model=schema_class,
    )