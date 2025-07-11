const express = require("express");
const axios = require("axios");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(express.json());

const LOG_DIR = path.resolve(__dirname, "logs");
const LOG_FILE = path.join(LOG_DIR, "log.jsonl");

if (!fs.existsSync(LOG_DIR)) {
  fs.mkdirSync(LOG_DIR, { recursive: true });
  console.log("[app.js] Created logs directory");
}

// Proxy normal generate request
app.post("/generate", async (req, res) => {
  const { prompt } = req.body;

  if (!prompt || typeof prompt !== "string") {
    return res.status(400).json({ error: "Invalid or missing prompt" });
  }

  try {
    const response = await axios.post("http://127.0.0.1:8080/generate", {
      prompt,
    });
    const { response: generated } = response.data;

    // Log interaction
    const logEntry = {
      timestamp: new Date().toISOString(),
      prompt,
      response: generated,
    };

    fs.appendFileSync(LOG_FILE, JSON.stringify(logEntry) + "\n");
    console.log("[app.js] Logged to", LOG_FILE);

    res.json({ response: generated });
  } catch (err) {
    console.error("[app.js] Error:", err.message || err);
    res.status(500).json({ error: "Error generating response" });
  }
});

// Proxy streaming generate request
app.post("/generate-stream", async (req, res) => {
  const { prompt } = req.body;
  console.log("[app.js] /generate-stream prompt:", prompt);

  if (!prompt || typeof prompt !== "string") {
    return res.status(400).json({ error: "Invalid or missing prompt" });
  }

  try {
    // Set headers for streaming
    res.setHeader("Content-Type", "text/plain; charset=utf-8");
    res.setHeader("Transfer-Encoding", "chunked");

    // Forward the request to backend streaming endpoint
    const response = await axios({
      method: "post",
      url: "http://127.0.0.1:8080/generate-stream",
      data: { prompt },
      responseType: "stream",
    });

    // Pipe the streaming response from backend to client directly
    response.data.pipe(res);

    // Optional: log the entire prompt + response after stream ends
    let fullResponse = "";
    response.data.on("data", (chunk) => {
      fullResponse += chunk.toString();
    });
    response.data.on("end", () => {
      const logEntry = {
        timestamp: new Date().toISOString(),
        prompt,
        response: fullResponse.trim(),
      };
      fs.appendFileSync(LOG_FILE, JSON.stringify(logEntry) + "\n");
      console.log("[app.js] Logged streamed interaction");
    });
  } catch (err) {
    console.error("[app.js] Streaming error:", err.message || err);
    if (!res.headersSent) {
      res.status(500).json({ error: "Error generating streamed response" });
    } else {
      res.end();
    }
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`[app.js] Proxy server running on http://localhost:${PORT}`);
});
