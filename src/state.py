from typing import TypedDict, List,Dict, Any

class AppState(TypedDict):

    resume_text : str
    job_description : str
    structured_resume: Dict[str, Any]
    plan : List[str]
    rewritten_bullets : List[List[str]]  # Changed to list of lists for per-job bullets
    cover_letter : str
    final_resume_text : str
    verification_passed : bool
    feedback : str
    retry_count: int
    ats_score: float  # New field for ATS score
    ats_breakdown: Dict[str, Any]  # New field for ATS scoring breakdown

