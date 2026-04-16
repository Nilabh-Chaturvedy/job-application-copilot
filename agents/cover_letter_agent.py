from src.llm_client import client
from src.config import OPENAI_MODEL

def cover_letter_agent(state):
    if "write_cover_letter" not in state["plan"]:
        state["cover_letter"]=""
        return state
    
    prompt=f""" Write a professional but persuasive cover letter based on the Job Description and Resume.
    Resume : {state['resume_text']}
    Job Description : {state['job_description']}
    Rules:
    - Use only facts supported by the resume
    - Keep it to 3 to 4 short paragraphs
    - Professional tone
    """

    response=client.responses.create(model=OPENAI_MODEL,input=prompt)

    state["cover_letter"] = (response.output_text or "").strip()
    
    return state




