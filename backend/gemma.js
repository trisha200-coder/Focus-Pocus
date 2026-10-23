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
      console.warn("[Focus-Pocus AI] Gemini API call failed, falling back to companion response:", error.message);
    }
  }

  // Dynamic intelligent companion response
  const lower = message.toLowerCase().trim();
  if (lower === "hi" || lower === "hii" || lower === "hello" || lower === "hey") {
    return "Hey there! Ready to crush some study goals today? 🌙 Tell me what subject you're working on, or ask me for a focus plan!";
  }
  if (lower.includes("data structure") || lower.includes("algorithm") || lower.includes("dsa")) {
    return "Data Structures & Algorithms is best studied with active problem solving! Pick 1 problem (Arrays, Linked Lists, or Trees), set the Focus Timer for 25 minutes, and write out the logic before coding.";
  }
  if (lower.includes("math")) {
    return "For Mathematics, don't just reread notes—active practice is key! Grab paper and solve 3 practice problems during this session.";
  }
  if (lower.includes("machine learning") || lower.includes("ml") || lower.includes("ai")) {
    return "Machine Learning concepts stick best with implementation. Pick one model or formula, spend 20 minutes understanding the intuition, and 5 minutes summarizing it in your own words.";
  }
  if (lower.includes("goal") || lower.includes("plan") || lower.includes("today")) {
    return "Let's set a realistic goal! Choose one priority subject and aim for a 25-minute focused session. You can take a 5-minute break right after.";
  }
  if (lower.includes("tired") || lower.includes("burnout") || lower.includes("stress")) {
    return "It's completely okay to feel tired. Try taking a deep breath, drinking a glass of water, and just committing to 5 easy minutes. You can always stop after that.";
  }
  if (lower.includes("distract") || lower.includes("phone") || lower.includes("focus")) {
    return "To beat distractions: turn off phone notifications, put it in another room, and start a 15-minute focus sprint right now.";
  }
  return `That sounds like a great study plan for "${message}". Break it down into one small task, set your timer for 25 minutes, and dive in! You've got this ✨`;
}

async function getStudyInsights(studyData) {
  if (ai) {
    try {
      const prompt = `
You are Focus-Pocus, an AI study-habit analyst.

Analyze the supplied study records and recommend which subject
the student should study next.

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

  if (!Array.isArray(studyData) || studyData.length === 0) {
    return {
      recommended_subject: null,
      observations: ["No subject records found."],
      reason: "Start by adding subjects and completing your first focus timer session.",
      suggested_minutes: 25,
      next_steps: ["Pick your most urgent subject", "Start a 25-minute session"]
    };
  }

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
