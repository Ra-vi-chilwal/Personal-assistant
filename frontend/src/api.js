const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function chat(question, history) {
  let res;
  try {
    res = await fetch(`${BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, history }),
    });
  } catch {
    throw new Error("I can't reach the server right now. Please try again in a moment.");
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(res.status === 429 ? data.detail : "Something went wrong on my side. Please try again.");
  }
  return data.answer;
}
