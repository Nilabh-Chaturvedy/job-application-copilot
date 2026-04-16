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
        "rewritten_bullets": [],
        "cover_letter": "",
        "verification_passed": False,
        "feedback": "",
        "retry_count": 0,
    }
    result=graph.invoke(initial_state)

print("\n---PLAN---")

print(result["plan"])

print("\n----Rewritten Bullets----")

for i,b in enumerate(result["rewritten_bullets"],1):
    print(f"{i},{b}")

print("\n--- COVER LETTER ---")
print(result["cover_letter"])

print("\n---verification check---")

print("passed",result["verification_passed"])
print("feedback",result["feedback"])

def save_separate_outputs(result):
    with open("tailored_bullets.txt", "w", encoding="utf-8") as f:
        for i, bullet in enumerate(result["rewritten_bullets"], 1):
            f.write(f"{i}. {bullet}\n")

    with open("cover_letter.txt", "w", encoding="utf-8") as f:
        f.write(result["cover_letter"])

save_separate_outputs(result)
