import os
from faster_whisper import WhisperModel

# Use 'base' for speed, 'small' or 'medium' for better accuracy
MODEL_SIZE = "base"

# Initialize model once (CPU for Mac/Generic, CUDA for NVIDIA)
device = "cuda" if os.getenv("USE_GPU") == "true" else "cpu"
model = WhisperModel(MODEL_SIZE, device=device, compute_type="int8")

def transcribe_audio(file_path: str) -> str:
    segments, info = model.transcribe(file_path, beam_size=5)
    full_text = " ".join([segment.text for segment in segments])
    return full_text.strip()