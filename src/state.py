from typing import TypedDict, List,Dict, Any

class AppState(TypedDict):

    resume_text : str
    job_description : str
    structured_resume: Dict[str, Any]
    plan : List[str]
    rewritten_bullets : List[str]
    cover_letter : str
    final_resume_text : str
    verification_passed : bool
    feedback : str
    retry_count: int

