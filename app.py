import os
import tempfile
import streamlit as st
from src.workflow import graph
from src.pdf_parser import extract_text_from_pdf

st.set_page_config(
    page_title="🚀 Job Application Copilot",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .input-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .output-container {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .success-container {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 25px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .instruction-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #667eea;
    }
    .bullet-point {
        background: rgba(255, 255, 255, 0.8);
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 4px solid #667eea;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with instructions
with st.sidebar:
    st.header("📋 How to Use")
    st.markdown("""
    <div class="instruction-box">
    <h4>🎯 Step 1: Upload Resume PDF</h4>
    <p>Upload your resume as a PDF file.</p>
    </div>

    <div class="instruction-box">
    <h4>📝 Step 2: Paste Job Description</h4>
    <p>Paste the complete job description you are applying for.</p>
    </div>

    <div class="instruction-box">
    <h4>🤖 Step 3: Generate Materials</h4>
    <p>The AI workflow will extract text, tailor resume bullets, generate a cover letter, and verify the result.</p>
    </div>
    """, unsafe_allow_html=True)

    st.header("🔧 Features")
    st.markdown("""
    - 📄 **PDF Upload**: Resume PDF support
    - ✨ **Smart Analysis**: AI-powered job matching
    - 📝 **Tailored Bullets**: Customized resume points
    - ✉️ **Cover Letter**: Personalized application letter
    - ✅ **Quality Check**: Built-in verification system
    - 💾 **Easy Export**: Download ready-to-use files
    """)

# Main content
st.markdown('<h1 class="main-header">🚀 Job Application Copilot</h1>', unsafe_allow_html=True)
st.markdown("### Upload your resume PDF and generate job-tailored application materials 💡")

# Input section
st.header("📥 Input Your Information")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.subheader("📄 Upload Resume PDF")
    uploaded_file = st.file_uploader(
        "Upload your resume PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.subheader("🎯 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="Copy and paste the complete job description from the posting...\n\nInclude:\n- Job title\n- Requirements\n- Responsibilities\n- etc.",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Generate button
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate = st.button("🚀 Generate Application Materials", use_container_width=True)

if generate:
    if uploaded_file is None or not job_description.strip():
        st.error("❌ Please upload a resume PDF and provide a job description.")
        st.warning("💡 Make sure both inputs are provided.")
    else:
        temp_pdf_path = None

        try:
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text("📄 Saving uploaded PDF...")
            progress_bar.progress(10)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_pdf_path = tmp_file.name

            status_text.text("🔍 Extracting text from resume PDF...")
            progress_bar.progress(25)

            resume_text = extract_text_from_pdf(temp_pdf_path)

            if not resume_text.strip():
                st.error("❌ Could not extract text from the uploaded PDF.")
                st.stop()

            status_text.text("🤖 Running AI planning agent...")
            progress_bar.progress(50)

            initial_state = {
                "resume_text": resume_text,
                "job_description": job_description,
                "structured_resume": {},
                "plan": [],
                "rewritten_bullets": [],
                "cover_letter": "",
                "final_resume_text": "",
                "verification_passed": False,
                "feedback": "",
                "retry_count": 0,
            }

            status_text.text("✍️ Generating tailored materials...")
            progress_bar.progress(75)

            with st.spinner("🎨 Finalizing your application materials..."):
                result = graph.invoke(initial_state)

            progress_bar.progress(100)
            status_text.text("✅ Application materials generated successfully!")
            progress_bar.empty()
            status_text.empty()

            # Optional debug section
            with st.expander("📄 Extracted Resume Text (Debug View)", expanded=False):
                st.text_area("Extracted Text", value=resume_text, height=300)

            # Results section
            st.header("🎉 Your Customized Application Materials")

            # Plan
            with st.expander("📋 AI Analysis Plan", expanded=True):
                st.markdown('<div class="output-container">', unsafe_allow_html=True)
                st.write("**AI's strategic approach:**")
                st.write(result.get("plan", []))
                st.markdown('</div>', unsafe_allow_html=True)

            # Resume Bullets
            st.subheader("📝 Tailored Resume Bullets")
            st.markdown('<div class="output-container">', unsafe_allow_html=True)

            bullets = result.get("rewritten_bullets", [])
            if bullets:
                for i, bullet in enumerate(bullets, 1):
                    st.markdown(f'<div class="bullet-point"><strong>{i}.</strong> {bullet}</div>', unsafe_allow_html=True)
            else:
                st.warning("No bullets were generated. Please check your resume and job description.")

            bullets_text = "\n".join([f"{i}. {b}" for i, b in enumerate(bullets, 1)])
            st.download_button(
                label="💾 Download Resume Bullets",
                data=bullets_text,
                file_name="tailored_resume_bullets.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # Cover Letter
            st.subheader("✉️ Generated Cover Letter")
            st.markdown('<div class="output-container">', unsafe_allow_html=True)
            cover_letter = result.get("cover_letter", "")
            st.text_area(
                "Your personalized cover letter:",
                value=cover_letter,
                height=300,
                disabled=True
            )

            st.download_button(
                label="💾 Download Cover Letter",
                data=cover_letter,
                file_name="generated_cover_letter.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # Final modified resume text
            final_resume_text = result.get("final_resume_text", "")
            if final_resume_text:
                st.subheader("📄 Modified Resume Draft")
                st.markdown('<div class="output-container">', unsafe_allow_html=True)
                st.text_area(
                    "Final modified resume text:",
                    value=final_resume_text,
                    height=350,
                    disabled=True
                )

                st.download_button(
                    label="💾 Download Modified Resume",
                    data=final_resume_text,
                    file_name="modified_resume.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

            # Verification
            st.subheader("✅ Quality Verification")
            if result.get("verification_passed", False):
                st.markdown('<div class="success-container">', unsafe_allow_html=True)
                st.success("🎉 Your application materials passed quality verification!")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Some improvements may be needed based on the verification feedback.")

            with st.expander("📊 Verification Details"):
                st.write("**Passed:**", result.get("verification_passed", False))
                st.write("**Feedback:**", result.get("feedback", ""))

            st.success("🎊 Your job application materials are ready! Download them above and customize as needed.")

        except Exception as e:
            st.error(f"❌ An error occurred while processing your resume: {str(e)}")

        finally:
            if temp_pdf_path and os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and LangGraph | Powered by OpenAI GPT")
st.markdown("💡 **Pro Tip:** Review and personalize the generated content before submitting your application!")