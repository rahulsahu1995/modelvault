# 🚀 MiniVault API – Offline Prompt/Response System

This project simulates a core feature of **ModelVault’s product**: receiving a prompt and returning a generated response — all offline using a **locally hosted LLM (Falcon RW 1B)**.

---

## 🛠️ Built With

- ⚡ **FastAPI** backend serving Falcon RW 1B
- 🔁 **Node.js proxy server** (folder: `minivault-api/`)
- 🐍 **Python CLI** for local testing
- 📝 **JSONL logging** in both backend and proxy layers

---

## 📁 Project Structure

modelvault/
├── python-code/
│ ├── server.py # FastAPI backend (LLM)
│ ├── cli.py # Python CLI for prompt testing
│ ├── logs/
│ │ └── log.jsonl # Backend logs
│ └── requirements.txt # Python dependencies
├── minivault-api/
│ ├── app.js # Node.js proxy server
│ ├── logs/
│ │ └── log.jsonl # Proxy server logs
│ └── package.json # Node dependencies
└----modelvault-testcases.postman_collection.json   #postman collection
|── README.md # This documentation

---

## 🧰 Setup Instructions

### 📦 1. Clone the Repository


```bash

git clone <your-repo-url>
cd modelvault


🧠 2. Python Backend (FastAPI)

✅ Setup Environment

cd python-code
python -m venv .venv
# Activate the environment:
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate


pip install -r requirements.txt
▶️ Run the FastAPI Server


uvicorn server:app --host 127.0.0.1 --port 8080
⚠️ First run will download Falcon RW 1B (~5.3GB) and cache it locally.



🌐 3. Node.js Proxy Server (minivault-api)


cd ../minivault-api
npm install
node app.js
Runs on: http://localhost:3000

Proxies to FastAPI backend on port 8080
Logs stored in: minivault-api/logs/log.jsonl


🧪 4. Test Using Python CLI

cd ../python-code
python cli.py --prompt "Tell me a joke."
python cli.py --prompt "What is artificial intelligence?" --stream
🌐 API Endpoints
🔹 POST /generate
URL: http://localhost:3000/generate


Request:

json
{
  "prompt": "What is the capital of France?"
}
Response:

json
{
  "response": "The capital of France is Paris."
}


🔸 POST /generate-stream


URL: http://localhost:3000/generate-stream

Behavior: Streams response character-by-character (or token-by-token) in plain text.

🧾 Logging
All interactions are stored as JSON lines.

✔️ Backend log: python-code/logs/log.jsonl
✔️ Proxy log: minivault-api/logs/log.jsonl


Example:
json
{
  "timestamp": "2025-07-11T10:34:02.912Z",
  "prompt": "Tell me a joke.",
  "response": "Why did the chicken cross the road?"
}

🧠 Model Details

Property	Description
Model	tiiuae/falcon-rw-1b
Size	~5.3GB
Runs Offline	✅ Yes (after first download)
Framework	Hugging Face Transformers
Features	Text generation, token streaming



🧪 Postman Collection (Optional Testing Tool)
You can test this API using the included Postman collection:

Collection Name: minivault-testcases

Endpoints Included:

POST /generate

POST /generate-stream


✅ How to Use:

Open Postman

Import the collection (minivault-testcases.json)

Set the prompt in the body (raw JSON)

Click Send and watch responses appear

🔁 For streaming responses,run this command on server side "python cli.py --prompt "What is the capital of France?" --stream" this will give streaming responses. 


