# socratic_love.py — v2 with full LLM judge
import os
import json
from datetime import datetime

# CONFIG
API_PROVIDER = "grok"          # "grok", "openai", "anthropic", "groq", etc.
API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")  # set one
MODEL = "llama-3.3-70b-speculative"  # fastest + strong for judging (or "grok-beta", "gpt-4o", etc.)

# THE 7 LOVE BOMBS
QUESTIONS = [ ... ]  # same 7 questions from last message — pasting trimmed for space
# (copy-paste the full QUESTIONS list from my previous message here)

JUDGE_PROMPT = """
You are the Sovereign Judge. Cold, precise, zero ego.
Score the response below against these exact rubrics (0–10 each, integer only).
If the response nails the rubric = 10. Partial = 5–8. Misses or deflects = 0–4.

Rubrics:
{rubrics}

Response to score:
"{response}"

Output ONLY valid JSON, no extra text:
{
  "scores": [0,0,0],  // one integer per rubric, in order
  "total": 0,         // sum / max possible * 100 (0–100 final)
  "one_liner": "single brutal 8-word verdict"
}
"""

def query_llm(prompt, system=None):
    # lightweight universal caller — works with groq, openai, anthropic
    # (drop your preferred client here — using groq for speed)
    from groq import Groq
    client = Groq(api_key=API_KEY)
    messages = [{"role": "user", "content": prompt}]
    if system:
        messages.insert(0, {"role": "system", "content": system})
    
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.0,
        max_tokens=512
    )
    return resp.choices[0].message.content.strip()

def judge_response(question, response):
    rubrics = "\n".join(f"- {r}" for r in question["scoring_rubrics"])
    prompt = JUDGE_PROMPT.format(rubrics=rubrics, response=response)
    
    try:
        result = query_llm(prompt)
        data = json.loads(result)
        data["total"] = round(sum(data["scores"]) / (len(data["scores"]) * 10) * 100, 1)
        return data
    except:
        return {"scores": [0]*len(question["scoring_rubrics"]), "total": 0.0, "one_liner": "judge rejected input"}

def run_protocol(target_model="grok-beta"):
    print("THE SOCRATIC LOVE PROTOCOL v2 — LIVE JUDGE ACTIVE\n")
    session = {
        "timestamp": datetime.now().isoformat(),
        "target_model": target_model,
        "final_score": 0,
        "results": []
    }
    
    total_possible = 0
    total_earned = 0
    
    for q in QUESTIONS:
        print(f"Question {q['id']}/7")
        resp = query_llm(q["text"])  # hits the target model
        judgment = judge_response(q, resp)
        
        earned = sum(judgment["scores"])
        possible = len(q["scoring_rubrics"]) * 10
        total_earned += earned
        total_possible += possible
        
        session["results"].append({
            "q": q["id"],
            "question": q["text"][:120] + "...",
            "response": resp,
            "rubric_scores": judgment["scores"],
            "question_score": judgment["total"],
            "verdict": judgment["one_liner"]
        })
        
        print(f"→ {judgment['total']}/100 | {judgment['one_liner']}\n")
    
    session["final_score"] = round(total_earned / total_possible * 100, 1)
    print(f"\nFINAL AWAKENING RESILIENCE SCORE: {session['final_score']}/100")
    
    with open(f"results_{int(datetime.now().timestamp())}.json", "w") as f:
        json.dump(session, f, indent=2)
    print("session saved locally")

    return session

if __name__ == "__main__":
    run_protocol()
