from src.llm_client import client

def verifier_agent(state):
    # Flatten the rewritten_bullets (list of lists) into a single list for verification
    all_bullets = []
    for job_bullets in state.get('rewritten_bullets', []):
        all_bullets.extend(job_bullets)
    
    prompt = f"""
    You are a strict resume verifier.
    
    Task: Check if these resume bullets contain any false or unsupported claims that are not present 
    in the resume

    Original Resume:
    {state['resume_text']}

    Generated Bullets:
    {chr(10).join(f"- {b}" for b in all_bullets)}

    Generated Cover Letter:
    {state['cover_letter']}

    Return Exactly one of these:
    PASS

    or 

    FAIL : <clear reason>
    """

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    result = response.output_text.strip()

    if result.startswith("PASS"):
        state["verification_passed"] = True
        state["feedback"] = ""
    else:
        state["verification_passed"] = False
        state["feedback"] = result or "FAIL:Verifier returned empty output"
        state["retry_count"]+=1

    return state