from src.llm_client import client
from src.config import OPENAI_MODEL


def writer_agent(state):
    if "rewrite_bullets" not in state["plan"]:
        state["rewritten_bullets"] = []
        return state

    structured_resume = state["structured_resume"]
    experiences = structured_resume.get("experience", [])
    
    all_bullets = []
    
    for i, exp in enumerate(experiences):
        prompt = f"""
You are an expert resume writer.

Job Experience #{i+1}:
Company: {exp.get('company', '')}
Role: {exp.get('role', '')}
Original Bullets:
{chr(10).join(f"- {b}" for b in exp.get('bullets', []))}

Job Description:
{state["job_description"]}

Task:
Rewrite 3-5 resume bullets for this specific job experience, tailored to the job description.

Rules:
- Use only facts supported by the original resume bullets
- Do not invent tools, metrics, or achievements
- Each bullet must be concise and resume-ready
- Start with a strong action verb
- Focus on business impact and technical ownership
- Keep each bullet under 35 words
- Incorporate relevant keywords from the job description
- Return one bullet per line
- Do not use labels like Situation, Task, Action, Result
"""

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=prompt
        )

        text = (response.output_text or "").strip()
        bullets = [line.strip("-• ").strip() for line in text.split("\n") if line.strip()]
        all_bullets.append(bullets)
    
    state["rewritten_bullets"] = all_bullets
    return state
