# MiniVault API – Offline Prompt/Response System

This project simulates a core feature of ModelVault’s product: receiving a prompt and returning a generated response — all offline, using a (locally hosted LLM) (Falcon RW 1B).

Built with:

- **FastAPI backend running** Falcon RW 1B
- **Node.js proxy server** (`minivault-api/`)
- **Python CLI** for prompt testing
- **Local logging** in both backend and proxy layers

---

📁 Project Structure

modelvault/
├── python-code/
│ ├── server.py # FastAPI backend using Falcon RW 1B
│ ├── cli.py # Python CLI for prompt testing
│ ├── logs/
│ │ └── log.jsonl # Backend logs (prompt + response)
│ └── requirements.txt # Python dependencies
├── minivault-api/ # Node.js proxy server
│ ├── app.js # Express server that proxies to FastAPI
│ ├── logs/
│ │ └── log.jsonl # Node proxy logs
│ └── package.json # Node.js dependencies
└── README.md # This documentation

## 🚀 Setup Instructions

## 1. Clone the Repository

```bash
git clone <your-repo-url>
cd modelvault
2. Python Backend (FastAPI)
Setup Environment

cd python-code

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt

Run FastAPI Server

uvicorn server:app --host 127.0.0.1 --port 8080
On first run, Falcon RW 1B model (~5.3GB) will download and be cached.

3. Node.js Proxy Server (minivault-api)

cd ../minivault-api
npm install
node app.js
Runs on: http://localhost:3000

Forwards requests to FastAPI backend on port 8080

Logs to: minivault-api/logs/log.jsonl

4. Test with Python CLI

cd ../python-code
python cli.py --prompt "Tell me a joke."
python cli.py --prompt "What is artificial intelligence?" --stream API Endpoints
POST /generate
URL: http://localhost:3000/generate

Request:

json
{ "prompt": "What is the capital of France?" }
Response:

json
{ "response": "The capital of France is...." }
POST /generate-stream
URL: http://localhost:3000/generate-stream

Streams text token-by-token as plain text output.

🧾 Logging
All interactions are saved locally in JSON Lines (.jsonl) format.

Backend: python-code/logs/log.jsonl

Node Proxy: minivault-api/logs/log.jsonl

Each log contains:

json

{
  "timestamp": "2025-07-11T10:34:02.912Z",
  "prompt": "Tell me a joke.",
  "response": "Why did the chicken cross the road..."
}

## Model Info
Model: tiiuae/falcon-rw-1b

Runs Locally: (no internet needed after first download)

Framework: Hugging Face Transformers

Model Size: -5.3GB

Supports: Token-by-token streaming, text generation

Features
Offline LLM using Falcon RW 1B

Proxy architecture with FastAPI + Node.js

POST and streaming endpoints

Prompt/response logging on both ends

CLI for testing without a frontend
```
