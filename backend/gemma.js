const { GoogleGenAI } = require("@google/genai");

let ai = null;
const apiKey = process.env.GEMINI_API_KEY;

if (apiKey && apiKey !== "your_gemini_api_key_here") {
  try {
    ai = new GoogleGenAI({ apiKey });
  } catch (err) {
    console.warn("[Focus-Pocus AI] Failed to initialize GoogleGenAI client:", err.message);
  }
}

async function getStudyResponse(message) {
  if (ai) {
    try {
      const prompt = `
You are Focus-Pocus, a friendly AI study companion.

Help students overcome procrastination without judgment.
Create realistic study plans, use active recall and spaced repetition,
and encourage sustainable study habits.
Ask clarifying questions when important information is missing.
Do not initiate messages on your own.

Student's message:
${message}

Respond helpfully, naturally, and concisely.
`;
      const modelName = process.env.GEMINI_MODEL || "gemini-2.5-flash";
      const response = await ai.models.generateContent({
        model: modelName,
        contents: prompt,
      });

      if (response && response.text) {
        return response.text;
      }
    } catch (error) {
      console.warn("[Focus-Pocus AI] Gemini API call failed, falling back to local companion:", error.message);
    }
  }

  // Graceful intelligent local fallback when Gemini API key is not present or offline
  const lower = message.toLowerCase();
  if (lower.includes("goal") || lower.includes("plan") || lower.includes("today")) {
    return "Let's set a realistic goal! Pick one subject and aim for a 25-minute focused session. You can take a 5-minute break right after.";
  }
  if (lower.includes("tired") || lower.includes("burnout") || lower.includes("stress")) {
    return "It's completely okay to feel tired. Try taking a deep breath, drinking a glass of water, and just committing to 5 easy minutes. You can always stop after that.";
  }
  if (lower.includes("distract") || lower.includes("phone") || lower.includes("focus")) {
    return "To beat distractions: turn off phone notifications, put it across the room, and use the Focus Timer for one single sprint.";
  }
  return "You're doing great just by showing up! Break your work down into the smallest possible step, start your timer, and take it one session at a time ✨";
}

async function getStudyInsights(studyData) {
  if (ai) {
    try {
      const prompt = `
You are Focus-Pocus, an AI study-habit analyst.

Analyze the supplied study records and recommend which subject
the student should study next.

Use these rules:
- Prioritize subjects with less recent study time.
- Consider how long it has been since each subject was studied.
- Compare subjects fairly using the amount of recorded study time.
- Explain the evidence behind each recommendation.
- Do not invent exam dates, difficulty levels, grades, or study sessions.
- If there is insufficient data, clearly say so.
- Treat an unstudied subject as needing attention, not as proof that
  the student is struggling with it.
- Give practical, realistic next steps.

Return valid JSON only, using this structure:
{
  "recommended_subject": "subject name or null",
  "observations": ["observation 1", "observation 2"],
  "reason": "why this subject is recommended",
  "suggested_minutes": 30,
  "next_steps": ["step 1", "step 2"]
}

Study records:
${JSON.stringify(studyData)}
`;
      const modelName = process.env.GEMINI_MODEL || "gemini-2.5-flash";
      const response = await ai.models.generateContent({
        model: modelName,
        contents: prompt,
      });

      const text = (response.text || "").trim();
      const cleaned = text
        .replace(/^```(?:json)?\s*/i, "")
        .replace(/\s*```$/, "");

      return JSON.parse(cleaned);
    } catch (error) {
      console.warn("[Focus-Pocus AI] Gemini insights failed, falling back to heuristic insights:", error.message);
    }
  }

  // Graceful rule-based analysis fallback
  if (!Array.isArray(studyData) || studyData.length === 0) {
    return {
      recommended_subject: null,
      observations: ["No subject records found."],
      reason: "Start by adding subjects and completing your first focus timer session.",
      suggested_minutes: 25,
      next_steps: ["Pick your most urgent subject", "Start a 25-minute session"]
    };
  }

  // Find subject with least minutes
  const sorted = [...studyData].sort((a, b) => (a.total_minutes || 0) - (b.total_minutes || 0));
  const recommended = sorted[0];

  return {
    recommended_subject: recommended.subject,
    observations: [
      `You've spent ${recommended.total_minutes || 0} minutes on ${recommended.subject}.`,
      `Total subjects tracked: ${studyData.length}.`
    ],
    reason: `${recommended.subject} currently has the lowest total study time and could use some attention.`,
    suggested_minutes: 25,
    next_steps: [
      `Open Focus Timer for ${recommended.subject}`,
      "Complete one 25-minute Pomodoro session",
      "Take a 5-minute restorative break"
    ]
  };
}

module.exports = { getStudyResponse, getStudyInsights };
