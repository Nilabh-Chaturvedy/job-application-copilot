import streamlit as st
from src.workflow import graph


st.set_page_config(page_title="Job Application Copilot", layout="wide")

st.title("Job Application Copilot")
st.write("Upload your resume text and paste a job description to generate tailored bullets and a cover letter.")

# Inputs
resume_text = st.text_area("Resume Text", height=300, placeholder="Paste your resume here...")
job_description = st.text_area("Job Description", height=300, placeholder="Paste the JD here...")

generate = st.button("Generate Application Materials")

if generate:
    if not resume_text.strip() or not job_description.strip():
        st.error("Please provide both resume text and job description.")
    else:
        with st.spinner("Running agent workflow..."):
            initial_state = {
                "resume_text": resume_text,
                "job_description": job_description,
                "plan": [],
                "rewritten_bullets": [],
                "cover_letter": "",
                "verification_passed": False,
                "feedback": "",
                "retry_count": 0,
            }

            result = graph.invoke(initial_state)

        st.subheader("Plan")
        st.write(result["plan"])

        st.subheader("Tailored Resume Bullets")
        for i, bullet in enumerate(result["rewritten_bullets"], 1):
            st.markdown(f"**{i}.** {bullet}")

        st.subheader("Cover Letter")
        st.text_area("Generated Cover Letter", value=result["cover_letter"], height=300)

        st.subheader("Verification")
        st.write("Passed:", result["verification_passed"])
        st.write("Feedback:", result["feedback"])

        # Downloads
        bullets_text = "\n".join([f"{i}. {b}" for i, b in enumerate(result["rewritten_bullets"], 1)])

        st.download_button(
            label="Download Bullets",
            data=bullets_text,
            file_name="tailored_bullets.txt",
            mime="text/plain"
        )

        st.download_button(
            label="Download Cover Letter",
            data=result["cover_letter"],
            file_name="cover_letter.txt",
            mime="text/plain"
        )