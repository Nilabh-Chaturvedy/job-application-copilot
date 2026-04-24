from src.workflow import graph


def read_text_file(path:str)->str:
    with open(path,"r",encoding="utf-8") as f:
        return f.read()



if __name__ == "__main__":

    resume_text=read_text_file("data/resume.txt")
    jd_text=read_text_file("data/jd.txt")

    initial_state = {
        "resume_text": resume_text,
        "job_description": jd_text,
        "plan": [],
        "rewritten_bullets": [],  # Now a list of lists
        "cover_letter": "",
        "verification_passed": False,
        "feedback": "",
        "retry_count": 0,
        "ats_score": 0.0,
        "ats_breakdown": {},
    }
    result=graph.invoke(initial_state)

print("\n---PLAN---")

print(result["plan"])

print("\n----Rewritten Bullets----")

for i, job_bullets in enumerate(result["rewritten_bullets"], 1):
    print(f"Job {i}:")
    for j, bullet in enumerate(job_bullets, 1):
        print(f"  {j}. {bullet}")
    print()

print("\n--- COVER LETTER ---")
print(result["cover_letter"])

print("\n---verification check---")

print("passed",result["verification_passed"])
print("feedback",result["feedback"])

print("\n--- ATS SCORING ---")
print(f"Overall ATS Score: {result['ats_score']}/100")
print("Breakdown:")
print(f"  Keyword Match: {result['ats_breakdown'].get('keyword_match', 0)}/100")
print(f"  Formatting: {result['ats_breakdown'].get('formatting', 0)}/100")
print(f"  Skills Alignment: {result['ats_breakdown'].get('skills_alignment', 0)}/100")
print(f"  Matched Keywords: {', '.join(result['ats_breakdown'].get('matched_keywords', []))}")
print(f"  Missing Keywords: {', '.join(result['ats_breakdown'].get('missing_keywords', []))}")

def save_separate_outputs(result):
    with open("tailored_bullets.txt", "w", encoding="utf-8") as f:
        for i, job_bullets in enumerate(result["rewritten_bullets"], 1):
            f.write(f"Job {i}:\n")
            for j, bullet in enumerate(job_bullets, 1):
                f.write(f"{j}. {bullet}\n")
            f.write("\n")

    with open("cover_letter.txt", "w", encoding="utf-8") as f:
        f.write(result["cover_letter"])
    
    with open("ats_score.txt", "w", encoding="utf-8") as f:
        f.write(f"ATS Score: {result['ats_score']}/100\n\n")
        f.write("Breakdown:\n")
        f.write(f"Keyword Match: {result['ats_breakdown'].get('keyword_match', 0)}/100\n")
        f.write(f"Formatting: {result['ats_breakdown'].get('formatting', 0)}/100\n")
        f.write(f"Skills Alignment: {result['ats_breakdown'].get('skills_alignment', 0)}/100\n\n")
        f.write(f"Matched Keywords: {', '.join(result['ats_breakdown'].get('matched_keywords', []))}\n")
        f.write(f"Missing Keywords: {', '.join(result['ats_breakdown'].get('missing_keywords', []))}\n")

save_separate_outputs(result)
