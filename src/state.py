from typing import TypedDict, List

class AppState(TypedDict):

    resume_text : str
    job_description : str
    plan : List[str]
    rewritten_bullets : List[str]
    cover_letter : str
    verification_passed : bool
    feedback : str
    retry_count: int

    