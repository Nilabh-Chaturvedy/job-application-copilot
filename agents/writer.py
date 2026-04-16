from src.llm_client import client
from src.config import OPENAI_MODEL


def writer_agent(state):
    if "rewrite_bullets" not in state["plan"]:
        state["rewritten_bullets"] = []
        return state

    prompt = f"""
You are an expert resume writer.

Candidate Resume:
{state["resume_text"]}

Job Description:
{state["job_description"]}

Task:
Rewrite 5 resume bullets tailored to the job description.

Rules:
- Use only facts supported by the resume
- Do not invent tools, metrics, or achievements
- Each bullet must be concise and resume-ready
- Start with a strong action verb
- Focus on business impact and technical ownership
- Keep each bullet under 35 words
- Return one bullet per line
- Do not use labels like Situation, Task, Action, Result
"""

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt
    )

    text = (response.output_text or "").strip()
    bullets = [line.strip("-• ").strip() for line in text.split("\n") if line.strip()]
    state["rewritten_bullets"] = bullets
    return state