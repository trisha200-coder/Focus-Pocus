require("dotenv").config();

const express = require("express");
const cors = require("cors");
const { getStudyResponse } = require("./gemma");

const app = express();

app.use(cors());
app.use(express.json({ limit: "20kb" }));

app.get("/", (req, res) => {
  res.json({ message: "Focus-Pocus AI backend is running." });
});

app.post("/api/chat", async (req, res) => {
  try {
    const { message } = req.body || {};

    if (typeof message !== "string" || !message.trim()) {
      return res.status(400).json({ error: "Please enter a message." });
    }

    if (message.length > 4000) {
      return res.status(400).json({ error: "Message is too long." });
    }

    const reply = await getStudyResponse(message.trim());
    res.json({ reply });
  } catch (error) {
    console.error("AI request failed:", error.message);
    res.status(500).json({
      error: "The AI assistant is temporarily unavailable. Please try again."
    });
  }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Focus-Pocus backend running at http://localhost:${PORT}`);
});
