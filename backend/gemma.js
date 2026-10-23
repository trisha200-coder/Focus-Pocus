const { GoogleGenAI } = require("@google/genai");

let ai = null;
const apiKey = process.env.GEMINI_API_KEY;

if (apiKey && apiKey.trim().length > 10 && !apiKey.includes("your_gemini_api_key")) {
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
You are Focus-Pocus, a friendly, highly intelligent AI study companion.

Help students overcome procrastination, plan their study schedules, understand subjects, and use proven techniques (active recall, spaced repetition, Pomodoro).
Respond helpfully, naturally, and concisely in 2-3 short paragraphs or bullet points.

Student's question: ${message}
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
      console.warn("[Focus-Pocus AI] Gemini API call failed, using smart advisor:", error.message);
    }
  }

  // Highly intelligent conversational advisor engine
  const q = message.toLowerCase().trim();

  // Planning & scheduling (handling typos like "paln", "plan", "schedule", "routine")
  if (q.includes("plan") || q.includes("paln") || q.includes("schedule") || q.includes("routine") || q.includes("how to study") || q.includes("how should")) {
    return "Here is a high-impact study plan you can start right now:\n\n" +
           "1. **Rule of 3**: Pick just 3 key concepts or subtopics to master today.\n" +
           "2. **25/5 Pomodoro Cycle**: Set the Focus Timer for 25 minutes of deep focus without phone or notifications, then take a 5-minute break.\n" +
           "3. **Active Recall**: Spend the last 5 minutes writing down everything you remember from memory rather than just passively reading notes.\n\n" +
           "Which topic would you like to tackle in your first 25-minute sprint?";
  }

  // Suggestions & tips ("any other suggestions", "tips", "what else", "advice", "more")
  if (q.includes("suggestion") || q.includes("tip") || q.includes("what else") || q.includes("more") || q.includes("advice") || q.includes("help me")) {
    return "Here are 3 game-changing study techniques that work wonders:\n\n" +
           "• **The Feynman Technique**: Teach the concept out loud in plain English as if explaining to a 10-year-old. Wherever you get stuck is where your gaps are.\n" +
           "• **The Blurting Method**: Read a page for 5 minutes, close your book, and write down every single detail you remember on a blank sheet.\n" +
           "• **Interleaving**: Instead of studying one subject for 6 hours straight, alternate between two related subjects. It keeps your brain alert and boosts retention.";
  }

  // Greetings
  if (q === "hi" || q === "hii" || q === "hello" || q === "hey" || q.startsWith("hello") || q.startsWith("hey")) {
    return "Hey there! Ready to make some great progress today? 🎯 Tell me what subject or topic you're working on, or ask me for a study plan!";
  }

  // Data Structures & Algorithms
  if (q.includes("data structure") || q.includes("algorithm") || q.includes("dsa") || q.includes("leetcode") || q.includes("code") || q.includes("coding")) {
    return "For Data Structures & Algorithms, practice beats passive reading every time:\n\n" +
           "1. **Pick 1 Pattern**: Focus on one pattern at a time (e.g. Two Pointers, Sliding Window, BFS/DFS).\n" +
           "2. **Dry Run on Paper**: Always trace an example with pen and paper before touching code.\n" +
           "3. **Timer Sprint**: Give yourself 20 minutes to solve it independently before looking at hints.";
  }

  // Mathematics
  if (q.includes("math") || q.includes("calculus") || q.includes("algebra") || q.includes("geometry") || q.includes("probability")) {
    return "For Mathematics:\n\n" +
           "• Don't just read formulas—create a 'Formula Cheat Sheet' with 1 example problem per formula.\n" +
           "• Solve at least 3 problems of increasing difficulty per session: 1 basic, 1 medium, 1 challenge question.\n" +
           "• Check where you made calculation mistakes and keep an 'Error Log'!";
  }

  // Exams & Revision
  if (q.includes("exam") || q.includes("test") || q.includes("revision") || q.includes("revise") || q.includes("prep")) {
    return "For Exam Preparation:\n\n" +
           "• **Past Papers First**: Spend 70% of your time solving past exam questions and mock tests under timed conditions.\n" +
           "• **High-Yield Topics**: Review previous year question frequency and prioritize the chapters with the highest weightage first.\n" +
           "• **Spaced Review**: Review tricky flashcards or notes 24 hours after learning them, and again 3 days later.";
  }

  // Procrastination & Tiredness
  if (q.includes("tired") || q.includes("burnout") || q.includes("stress") || q.includes("bored") || q.includes("lazy") || q.includes("procrastinat")) {
    return "When motivation is low, use the **2-Minute Rule**:\n\n" +
           "Tell yourself: 'I will only sit and study for 2 minutes.' Open the notebook and read just one paragraph. Most of the friction is in starting—once you begin, momentum takes over. Take a deep breath and start small!";
  }

  // Distraction
  if (q.includes("distract") || q.includes("phone") || q.includes("focus") || q.includes("concentrat")) {
    return "To lock in deep concentration:\n\n" +
           "1. Put your phone in another room (out of sight, out of mind).\n" +
           "2. Put on instrumental lo-fi or brown noise to block background sounds.\n" +
           "3. Open the **Focus Timer** in Focus Pocus and commit to just 1 session!";
  }

  // Default thoughtful advisor response
  return "That is a great study focus! To make the most of it:\n\n" +
         "1. Define your exact goal for the next 25 minutes (e.g. 'Read section 3.2 and take bullet notes').\n" +
         "2. Jump over to the **Focus Timer** page to start a distraction-free sprint.\n" +
         "3. Test yourself with active recall immediately afterward.\n\n" +
         "Let me know if you want tips on a specific subject or topic!";
}

async function getStudyInsights(studyData) {
  if (ai) {
    try {
      const prompt = `
You are Focus-Pocus, an AI study-habit analyst.
Analyze the supplied study records and recommend which subject the student should study next.

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
      console.warn("[Focus-Pocus AI] Gemini insights failed, using smart advisor:", error.message);
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
