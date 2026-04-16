import json
from src.llm_client import client
from src.config import OPENAI_MODEL
from src.schemas import StructuredResume


def structure_resume(resume_text: str) -> dict:
    prompt = f"""
You are a resume parsing assistant.

Convert the following resume into structured JSON.

Return ONLY valid JSON.

Schema:
{{
  "summary": "string",
  "experience": [
    {{
      "company": "string",
      "role": "string",
      "location": "string",
      "dates": "string",
      "bullets": ["string", "string"]
    }}
  ],
  "skills": ["string", "string"],
  "education": [
    {{
      "institution": "string",
      "degree": "string",
      "dates": "string"
    }}
  ]
}}

Resume:
{resume_text}
"""

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt
    )

    raw_text = (response.output_text or "").strip()
    parsed = json.loads(raw_text)

    validated = StructuredResume(**parsed)
    return validated.model_dump()