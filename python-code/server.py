import os
import json
import asyncio
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Optional: set cache dir for HF models
HF_CACHE_DIR = "C:/hf_cache"  # Change as needed
os.makedirs(HF_CACHE_DIR, exist_ok=True)
os.environ["HF_HOME"] = HF_CACHE_DIR

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "log.jsonl")
os.makedirs(LOG_DIR, exist_ok=True)

app = FastAPI(
    title="MiniVault API - Falcon RW 1B",
    description="Offline Falcon RW 1B with streaming and logging",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_NAME = "tiiuae/falcon-rw-1b"
print(f"[server.py] Loading {MODEL_NAME}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()
print(f"[server.py] Model loaded on {device}")

def generate_response(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            max_new_tokens=100,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text[len(prompt):].strip()

@app.get("/")
def health_check():
    return {"status": "Falcon RW 1B API running"}

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return {"response": "Error: Prompt is empty"}

    response_text = generate_response(prompt)

    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt": prompt,
        "response": response_text,
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    return {"response": response_text}

@app.post("/generate-stream")
async def generate_stream(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "").strip()
    if not prompt:
        async def empty():
            yield "Error: Prompt is empty"
        return StreamingResponse(empty(), media_type="text/plain")

    response_text = generate_response(prompt)
    tokens = response_text.split()

    async def stream():
        for token in tokens:
            yield token + " "
            await asyncio.sleep(0.05)

    return StreamingResponse(stream(), media_type="text/plain")
