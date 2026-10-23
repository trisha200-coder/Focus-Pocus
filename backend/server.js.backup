require("dotenv").config();

const express = require("express");
const cors = require("cors");
const supabase = require("./supabase");
const { getStudyResponse } = require("./gemma");

const app = express();

app.use(cors());
app.use(express.json({ limit: "20kb" }));

app.get("/", (req, res) => {
  res.json({ message: "Focus-Pocus AI backend is running." });
});

// Temporary single-user prototype.
// Add verified authentication before deploying publicly.
const PROTOTYPE_USER_ID = process.env.PROTOTYPE_USER_ID;

function requirePrototypeUser(req, res, next) {
  if (!PROTOTYPE_USER_ID) {
    return res.status(503).json({
      error: "Set PROTOTYPE_USER_ID in backend/.env first."
    });
  }
  req.userId = PROTOTYPE_USER_ID;
  next();
}

app.get("/api/subjects", requirePrototypeUser, async (req, res) => {
  try {
    const { data, error } = await supabase
      .from("subjects")
      .select("id, name")
      .eq("user_id", req.userId)
      .order("name");

    if (error) throw error;
    res.json({ subjects: data });
  } catch (error) {
    console.error("Loading subjects failed:", error.message);
    res.status(500).json({ error: "Could not load subjects." });
  }
});

app.post("/api/subjects", requirePrototypeUser, async (req, res) => {
  try {
    const name = typeof req.body?.name === "string"
      ? req.body.name.trim()
      : "";

    if (!name || name.length > 100) {
      return res.status(400).json({
        error: "Subject name must contain 1–100 characters."
      });
    }

    const { data, error } = await supabase
      .from("subjects")
      .insert({ user_id: req.userId, name })
      .select("id, name")
      .single();

    if (error) {
      if (error.code === "23505") {
        return res.status(409).json({
          error: "That subject already exists."
        });
      }
      throw error;
    }

    res.status(201).json({ subject: data });
  } catch (error) {
    console.error("Creating subject failed:", error.message);
    res.status(500).json({ error: "Could not create subject." });
  }
});

app.post("/api/study/check-in", requirePrototypeUser, async (req, res) => {
  try {
    const subjectId = Number(req.body?.subjectId);

    if (!Number.isSafeInteger(subjectId) || subjectId <= 0) {
      return res.status(400).json({
        error: "Provide a valid subjectId."
      });
    }

    const { data: subject, error: subjectError } = await supabase
      .from("subjects")
      .select("id")
      .eq("id", subjectId)
      .eq("user_id", req.userId)
      .maybeSingle();

    if (subjectError) throw subjectError;
    if (!subject) {
      return res.status(404).json({ error: "Subject not found." });
    }

    const { data, error } = await supabase
      .from("study_sessions")
      .insert({
        user_id: req.userId,
        subject_id: subjectId
      })
      .select("id, subject_id, check_in, check_out")
      .single();

    if (error?.code === "23505") {
      return res.status(409).json({
        error: "You already have an active study session. Check out first."
      });
    }
    if (error) throw error;

    res.status(201).json({ session: data });
  } catch (error) {
    console.error("Check-in failed:", error.message);
    res.status(500).json({ error: "Could not start study session." });
  }
});

app.post("/api/study/check-out", requirePrototypeUser, async (req, res) => {
  try {
    const sessionId = Number(req.body?.sessionId);

    if (!Number.isSafeInteger(sessionId) || sessionId <= 0) {
      return res.status(400).json({
        error: "Provide a valid sessionId."
      });
    }

    const { data: session, error: lookupError } = await supabase
      .from("study_sessions")
      .select("id, check_in, subject_id")
      .eq("id", sessionId)
      .eq("user_id", req.userId)
      .is("check_out", null)
      .maybeSingle();

    if (lookupError) throw lookupError;
    if (!session) {
      return res.status(404).json({
        error: "No active session found with that ID."
      });
    }

    const checkOut = new Date().toISOString();

    const { data, error } = await supabase
      .from("study_sessions")
      .update({ check_out: checkOut })
      .eq("id", session.id)
      .eq("user_id", req.userId)
      .is("check_out", null)
      .select("id, subject_id, check_in, check_out")
      .maybeSingle();

    if (error) throw error;
    if (!data) {
      return res.status(409).json({
        error: "This session has already been checked out."
      });
    }

    const durationMinutes = Math.max(
      0,
      (new Date(data.check_out) - new Date(data.check_in)) / 60000
    );

    res.json({
      session: data,
      durationMinutes: Math.round(durationMinutes * 100) / 100,
      shortSession: durationMinutes < 10,
      suggestion: durationMinutes < 10
        ? "That was a short session. If you need a break, take one; otherwise, feel free to continue."
        : null
    });
  } catch (error) {
    console.error("Check-out failed:", error.message);
    res.status(500).json({ error: "Could not end study session." });
  }
});

// Existing Gemini chat endpoint remains available.
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
