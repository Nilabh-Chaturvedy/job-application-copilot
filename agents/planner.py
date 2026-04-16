import json
from src.llm_client import client
from src.schemas import plan


def extract_json_text(text: str) -> str:
    text = (text or "").strip()

    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    elif text.startswith("```"):
        text = text[len("```"):].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text


def planner_agent(state):
    prompt = f"""
You are a workflow planner for a job application system.

Your job is ONLY to decide which tasks should be run.

Allowed step names:
- rewrite_bullets
- write_cover_letter

Return ONLY valid JSON in this exact format:
{{"steps":["rewrite_bullets","write_cover_letter"]}}

Rules:
- Do not write resume bullets
- Do not write a cover letter
- Do not explain anything
- Do not include markdown
- Only return the JSON object

Resume:
{state["resume_text"][:2500]}

Job Description:
{state["job_description"][:2500]}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    raw_text = response.output_text or ""
    print("\n--- RAW PLANNER OUTPUT ---")
    print(repr(raw_text))

    cleaned_text = extract_json_text(raw_text)

    if not cleaned_text:
        print("Planner returned empty output. Falling back to default plan.")
        state["plan"] = ["rewrite_bullets", "write_cover_letter"]
        return state

    try:
        data = json.loads(cleaned_text)
        plan_text= plan(**data)
        state["plan"] = plan_text.steps
    except Exception as e:
        print(f"Planner parsing failed: {e}")
        print("Falling back to default plan.")
        state["plan"] = ["rewrite bullets", "write cover letter"]

    return state