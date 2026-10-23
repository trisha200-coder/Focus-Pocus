const { GoogleGenAI } = require("@google/genai");

const ai = new GoogleGenAI({
  apiKey: process.env.GEMINI_API_KEY,
});

async function getStudyResponse(message) {
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

  const response = await ai.models.generateContent({
    model: "gemma-4-26b-a4b-it",
    contents: prompt,
  });

  return response.text || "I couldn't generate a response. Please try again.";
}

async function getStudyInsights(studyData) {
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

  const response = await ai.models.generateContent({
    model: "gemma-4-26b-a4b-it",
    contents: prompt,
  });

  const text = (response.text || "").trim();
  const cleaned = text
    .replace(/^```(?:json)?\s*/i, "")
    .replace(/\s*```$/, "");

  try {
    return JSON.parse(cleaned);
  } catch {
    throw new Error("Gemini returned an invalid study-insights response.");
  }
}

module.exports = { getStudyResponse, getStudyInsights };
