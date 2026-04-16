import streamlit as st
from src.workflow import graph

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
    .download-btn {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%) !important;
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
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="🚀 Job Application Copilot",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar with instructions
with st.sidebar:
    st.header("📋 How to Use")
    st.markdown("""
    <div class="instruction-box">
    <h4>🎯 Step 1: Prepare Your Documents</h4>
    <p>Copy and paste your resume text and the job description you're applying for.</p>
    </div>

    <div class="instruction-box">
    <h4>🤖 Step 2: AI Processing</h4>
    <p>Our AI agents will analyze your resume and the job requirements to create tailored content.</p>
    </div>

    <div class="instruction-box">
    <h4>📄 Step 3: Review & Download</h4>
    <p>Review the generated resume bullets and cover letter, then download them.</p>
    </div>
    """, unsafe_allow_html=True)

    st.header("🔧 Features")
    st.markdown("""
    - ✨ **Smart Analysis**: AI-powered job matching
    - 📝 **Tailored Bullets**: Customized resume points
    - ✉️ **Cover Letter**: Personalized application letter
    - ✅ **Quality Check**: Built-in verification system
    - 💾 **Easy Export**: Download ready-to-use files
    """)

# Main content
st.markdown('<h1 class="main-header">🚀 Job Application Copilot</h1>', unsafe_allow_html=True)
st.markdown("### Transform your job applications with AI-powered personalization 💡")

# Input section
st.header("📥 Input Your Information")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.subheader("📄 Resume Text")
    resume_text = st.text_area(
        "Paste your resume content here",
        height=300,
        placeholder="Copy and paste your full resume text here...\n\nExample:\n- Experience with Python development\n- 3+ years in data analysis\n- etc.",
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
    if not resume_text.strip() or not job_description.strip():
        st.error("❌ Please provide both resume text and job description to proceed.")
        st.warning("💡 Make sure to fill in both input boxes above.")
    else:
        # Progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("🔍 Analyzing your resume and job description...")
        progress_bar.progress(25)

        status_text.text("🤖 Running AI planning agent...")
        progress_bar.progress(50)

        status_text.text("✍️ Generating tailored resume bullets...")
        progress_bar.progress(75)

        # Run the workflow
        with st.spinner("🎨 Finalizing your application materials..."):
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

        progress_bar.progress(100)
        status_text.text("✅ Application materials generated successfully!")
        progress_bar.empty()
        status_text.empty()

        # Results section
        st.header("🎉 Your Customized Application Materials")

        # Plan
        with st.expander("📋 AI Analysis Plan", expanded=True):
            st.markdown('<div class="output-container">', unsafe_allow_html=True)
            st.write("**AI's strategic approach:**")
            st.write(result["plan"])
            st.markdown('</div>', unsafe_allow_html=True)

        # Resume Bullets
        st.subheader("📝 Tailored Resume Bullets")
        st.markdown('<div class="output-container">', unsafe_allow_html=True)

        if result["rewritten_bullets"]:
            for i, bullet in enumerate(result["rewritten_bullets"], 1):
                st.markdown(f'<div class="bullet-point"><strong>{i}.</strong> {bullet}</div>', unsafe_allow_html=True)
        else:
            st.warning("No bullets were generated. Please check your inputs.")

        # Download bullets
        bullets_text = "\n".join([f"{i}. {b}" for i, b in enumerate(result["rewritten_bullets"], 1)])
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
        st.text_area(
            "Your personalized cover letter:",
            value=result["cover_letter"],
            height=300,
            disabled=True
        )

        # Download cover letter
        st.download_button(
            label="💾 Download Cover Letter",
            data=result["cover_letter"],
            file_name="generated_cover_letter.txt",
            mime="text/plain",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Verification
        st.subheader("✅ Quality Verification")
        if result["verification_passed"]:
            st.markdown('<div class="success-container">', unsafe_allow_html=True)
            st.success("🎉 Your application materials passed quality verification!")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Some improvements may be needed based on the verification feedback.")

        with st.expander("📊 Verification Details"):
            st.write("**Passed:**", result["verification_passed"])
            st.write("**Feedback:**", result["feedback"])

        # Success message
        st.success("🎊 Your job application materials are ready! Download them above and customize as needed.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and LangGraph | Powered by OpenAI GPT")
st.markdown("💡 **Pro Tip:** Review and personalize the generated content before submitting your application!")

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