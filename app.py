import os
import tempfile

import streamlit as st

from src.docx_builder import build_docx_resume
from src.pdf_parser import extract_text_from_pdf
from src.workflow import graph


st.set_page_config(
    page_title="Job Application Copilot",
    page_icon=":briefcase:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_section_intro(title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="section-intro">
            <p class="section-kicker">{title}</p>
            <p class="section-copy">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_panel(title: str, body: str, tone: str = "default") -> None:
    st.markdown(
        f"""
        <div class="status-panel {tone}">
            <p class="status-title">{title}</p>
            <p class="status-copy">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
        :root {
            --bg-main: #060606;
            --bg-shell: #0b0b0d;
            --bg-card: rgba(20, 20, 24, 0.88);
            --bg-card-strong: rgba(28, 16, 18, 0.96);
            --bg-soft: rgba(255, 255, 255, 0.03);
            --border-soft: rgba(255, 255, 255, 0.08);
            --border-accent: rgba(173, 42, 57, 0.45);
            --text-main: #f6f1f2;
            --text-muted: #b8adb0;
            --text-dim: #8d8084;
            --red-main: #a61e2d;
            --red-hover: #c62e3f;
            --red-deep: #5f0f1a;
            --red-soft: rgba(166, 30, 45, 0.14);
            --green-soft: rgba(48, 132, 86, 0.18);
            --amber-soft: rgba(171, 107, 23, 0.18);
            --shadow-main: 0 24px 60px rgba(0, 0, 0, 0.42);
            --shadow-red: 0 18px 45px rgba(122, 17, 29, 0.28);
            --radius-xl: 28px;
            --radius-lg: 22px;
            --radius-md: 16px;
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(166, 30, 45, 0.18), transparent 28%),
                radial-gradient(circle at top left, rgba(82, 8, 17, 0.22), transparent 22%),
                linear-gradient(180deg, #050506 0%, #09090b 100%);
            color: var(--text-main);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stAppViewContainer"] > .main {
            background: transparent;
        }

        .block-container {
            max-width: 1220px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(14, 14, 17, 0.98) 0%, rgba(10, 10, 12, 0.98) 100%);
            border-right: 1px solid var(--border-soft);
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem;
        }

        h1, h2, h3, h4, h5, h6, p, label, div, span {
            color: var(--text-main);
        }

        .hero-shell {
            position: relative;
            overflow: hidden;
            padding: 2.4rem 2.6rem;
            margin-bottom: 1.75rem;
            border-radius: var(--radius-xl);
            background:
                linear-gradient(140deg, rgba(23, 23, 28, 0.97) 0%, rgba(14, 14, 17, 0.97) 65%, rgba(39, 15, 19, 0.98) 100%);
            border: 1px solid rgba(255, 255, 255, 0.06);
            box-shadow: var(--shadow-main), var(--shadow-red);
        }

        .hero-shell::after {
            content: "";
            position: absolute;
            inset: auto -8% -36% auto;
            width: 280px;
            height: 280px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(166, 30, 45, 0.22) 0%, rgba(166, 30, 45, 0.02) 68%, transparent 72%);
            pointer-events: none;
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.42rem 0.78rem;
            margin: 0 0 1rem 0;
            border: 1px solid rgba(198, 46, 63, 0.34);
            border-radius: 999px;
            background: rgba(166, 30, 45, 0.12);
            color: #f6c9cf;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .hero-title {
            margin: 0;
            font-size: clamp(2.3rem, 5vw, 3.8rem);
            font-weight: 700;
            line-height: 1.05;
            letter-spacing: -0.03em;
        }

        .hero-subtitle {
            max-width: 760px;
            margin: 0.95rem 0 1.35rem 0;
            color: var(--text-muted);
            font-size: 1.05rem;
            line-height: 1.75;
        }

        .hero-stats {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
        }

        .hero-stat {
            padding: 1rem 1.05rem;
            border-radius: var(--radius-md);
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
        }

        .hero-stat-label {
            margin: 0;
            color: var(--text-dim);
            font-size: 0.76rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .hero-stat-value {
            margin: 0.35rem 0 0 0;
            font-size: 1.02rem;
            font-weight: 600;
            color: var(--text-main);
        }

        .sidebar-title {
            margin: 0 0 0.75rem 0;
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .sidebar-intro {
            margin: 0 0 1rem 0;
            color: var(--text-muted);
            line-height: 1.6;
        }

        .sidebar-card {
            padding: 1rem 1rem 1.05rem 1rem;
            margin: 0 0 0.85rem 0;
            border-radius: 18px;
            border: 1px solid var(--border-soft);
            background:
                linear-gradient(180deg, rgba(255, 255, 255, 0.035) 0%, rgba(255, 255, 255, 0.018) 100%);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
        }

        .sidebar-card h4 {
            margin: 0 0 0.4rem 0;
            font-size: 0.95rem;
        }

        .sidebar-card p,
        .sidebar-card li {
            margin: 0;
            color: var(--text-muted);
            line-height: 1.65;
        }

        .sidebar-list {
            margin: 0;
            padding-left: 1.1rem;
        }

        .section-intro {
            margin: 0.2rem 0 0.9rem 0;
        }

        .section-kicker {
            margin: 0;
            color: #f0cad0;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.11em;
            text-transform: uppercase;
        }

        .section-copy {
            margin: 0.45rem 0 0 0;
            color: var(--text-muted);
            line-height: 1.7;
        }

        .panel-card {
            padding: 1.4rem 1.35rem;
            margin: 0.45rem 0 0.85rem 0;
            border-radius: var(--radius-lg);
            background:
                linear-gradient(180deg, rgba(24, 24, 28, 0.94) 0%, rgba(17, 17, 20, 0.95) 100%);
            border: 1px solid var(--border-soft);
            box-shadow: var(--shadow-main);
        }

        .panel-card strong {
            color: var(--text-main);
        }

        .panel-title {
            margin: 0 0 0.35rem 0;
            font-size: 1.08rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .panel-description {
            margin: 0 0 1rem 0;
            color: var(--text-muted);
            line-height: 1.65;
        }

        .bullet-point {
            padding: 0.95rem 1rem;
            margin: 0.5rem 0;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-left: 4px solid var(--red-main);
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.04) 0%, rgba(166, 30, 45, 0.08) 100%);
            box-shadow: 0 14px 30px rgba(0, 0, 0, 0.22);
            color: var(--text-main);
        }

        .experience-label {
            margin-top: 1rem;
            color: #f4dde0;
            font-size: 0.95rem;
            font-weight: 700;
            letter-spacing: 0.01em;
        }

        .status-panel {
            padding: 1rem 1.1rem;
            margin: 0.45rem 0 0.9rem 0;
            border-radius: 16px;
            border: 1px solid var(--border-soft);
            background: rgba(255, 255, 255, 0.03);
            box-shadow: 0 14px 34px rgba(0, 0, 0, 0.2);
        }

        .status-panel.success {
            background: linear-gradient(180deg, rgba(48, 132, 86, 0.16) 0%, rgba(22, 58, 41, 0.22) 100%);
            border-color: rgba(77, 165, 115, 0.25);
        }

        .status-panel.warning {
            background: linear-gradient(180deg, rgba(171, 107, 23, 0.15) 0%, rgba(78, 48, 8, 0.18) 100%);
            border-color: rgba(222, 145, 45, 0.22);
        }

        .status-panel.default {
            background: linear-gradient(180deg, rgba(166, 30, 45, 0.14) 0%, rgba(56, 14, 21, 0.18) 100%);
            border-color: rgba(198, 46, 63, 0.24);
        }

        .status-title {
            margin: 0 0 0.25rem 0;
            font-size: 1rem;
            font-weight: 700;
        }

        .status-copy {
            margin: 0;
            color: var(--text-muted);
            line-height: 1.6;
        }

        .metric-card {
            padding: 1rem 1rem 1.05rem 1rem;
            border-radius: 18px;
            border: 1px solid var(--border-soft);
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.035) 0%, rgba(255, 255, 255, 0.015) 100%);
            box-shadow: 0 14px 32px rgba(0, 0, 0, 0.2);
        }

        .metric-card p {
            margin: 0;
        }

        .metric-card .metric-label {
            margin-bottom: 0.35rem;
            color: var(--text-dim);
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.11em;
            text-transform: uppercase;
        }

        .metric-card .metric-value {
            font-size: 1.45rem;
            font-weight: 700;
            color: var(--text-main);
        }

        .metric-card .metric-copy {
            margin-top: 0.35rem;
            color: var(--text-muted);
            line-height: 1.5;
        }

        .keyword-list {
            margin: 0.8rem 0 0 0;
            padding-left: 1.15rem;
        }

        .keyword-list li {
            margin-bottom: 0.35rem;
            color: var(--text-muted);
        }

        .download-row {
            margin-top: 1rem;
        }

        .footer-shell {
            margin-top: 2rem;
            padding: 1.35rem 1.4rem;
            border-radius: 18px;
            border: 1px solid var(--border-soft);
            background: linear-gradient(180deg, rgba(17, 17, 20, 0.94) 0%, rgba(12, 12, 14, 0.94) 100%);
        }

        .footer-shell p {
            margin: 0.2rem 0;
        }

        .footer-title {
            color: var(--text-main);
            font-weight: 700;
        }

        .footer-copy {
            color: var(--text-muted);
        }

        [data-testid="stFileUploader"] {
            border-radius: 18px;
        }

        [data-testid="stFileUploader"] section {
            padding: 1.2rem;
            border-radius: 18px;
            border: 1px dashed rgba(198, 46, 63, 0.34);
            background: linear-gradient(180deg, rgba(166, 30, 45, 0.08) 0%, rgba(255, 255, 255, 0.015) 100%);
        }

        [data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] span {
            color: var(--text-muted) !important;
        }

        .stButton > button,
        .stDownloadButton > button {
            min-height: 3rem;
            border-radius: 999px;
            border: 1px solid rgba(221, 77, 94, 0.22);
            background: linear-gradient(135deg, #8d1826 0%, #c62e3f 100%);
            color: #fff7f8;
            font-size: 0.96rem;
            font-weight: 700;
            letter-spacing: 0.01em;
            box-shadow: 0 18px 38px rgba(126, 17, 29, 0.26);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            border-color: rgba(239, 123, 136, 0.45);
            background: linear-gradient(135deg, #a61e2d 0%, #d53a4c 100%);
            transform: translateY(-1px);
            box-shadow: 0 22px 42px rgba(126, 17, 29, 0.32);
        }

        .stButton > button:focus,
        .stDownloadButton > button:focus {
            outline: none;
            box-shadow: 0 0 0 0.18rem rgba(198, 46, 63, 0.18), 0 22px 42px rgba(126, 17, 29, 0.32);
        }

        .stTextArea textarea {
            min-height: 260px;
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.03);
            color: var(--text-main);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.02);
        }

        .stTextArea textarea::placeholder {
            color: #8f8386;
        }

        .stTextArea textarea:focus,
        .stTextArea textarea:focus-visible {
            border-color: rgba(198, 46, 63, 0.45);
            box-shadow: 0 0 0 0.16rem rgba(198, 46, 63, 0.16);
        }

        [data-baseweb="base-input"] {
            background: transparent !important;
        }

        .stExpander {
            border-radius: 18px;
            border: 1px solid var(--border-soft);
            background: rgba(255, 255, 255, 0.02);
            box-shadow: 0 16px 34px rgba(0, 0, 0, 0.18);
        }

        .stExpander summary {
            color: var(--text-main);
        }

        [data-testid="stMetric"] {
            padding: 1rem 1rem 0.85rem 1rem;
            border-radius: 18px;
            border: 1px solid var(--border-soft);
            background: rgba(255, 255, 255, 0.025);
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"] {
            color: var(--text-main);
        }

        [data-testid="stMarkdownContainer"] hr {
            border-color: rgba(255, 255, 255, 0.08);
        }

        [data-testid="stAlert"] {
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            background: rgba(255, 255, 255, 0.04);
        }

        [data-testid="stProgressBar"] > div > div {
            background: linear-gradient(90deg, #7c1522 0%, #cb3344 100%);
        }

        @media (max-width: 900px) {
            .hero-shell {
                padding: 1.6rem 1.35rem;
            }

            .hero-stats {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.markdown('<p class="sidebar-title">Application Console</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sidebar-intro">A darker, cleaner workspace for tailoring resumes, cover letters, and ATS-ready application assets.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="sidebar-card">
            <h4>1. Upload Resume</h4>
            <p>Provide a PDF resume to extract and restructure your source material.</p>
        </div>
        <div class="sidebar-card">
            <h4>2. Paste Job Description</h4>
            <p>Use the complete posting so the workflow can optimize bullets, cover letter language, and keyword alignment.</p>
        </div>
        <div class="sidebar-card">
            <h4>3. Generate and Export</h4>
            <p>Review the tailored outputs, verification feedback, ATS score, and download the finished files.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<p class="sidebar-title">Included Outputs</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sidebar-card">
            <ul class="sidebar-list">
                <li>Tailored experience bullets</li>
                <li>Personalized cover letter</li>
                <li>Structured DOCX resume export</li>
                <li>Verification feedback and ATS scoring</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <section class="hero-shell">
        <p class="eyebrow">Premium Application Studio</p>
        <h1 class="hero-title">Job Application Copilot</h1>
        <p class="hero-subtitle">
            Transform a base resume into a polished job-specific package with a professional, dark workspace
            built for focused review, stronger hierarchy, and premium export-ready presentation.
        </p>
        <div class="hero-stats">
            <div class="hero-stat">
                <p class="hero-stat-label">Inputs</p>
                <p class="hero-stat-value">Resume PDF and target job brief</p>
            </div>
            <div class="hero-stat">
                <p class="hero-stat-label">Outputs</p>
                <p class="hero-stat-value">Bullets, cover letter, DOCX resume, ATS review</p>
            </div>
            <div class="hero-stat">
                <p class="hero-stat-label">Focus</p>
                <p class="hero-stat-value">Professional tone, clarity, and keyword alignment</p>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

render_section_intro(
    "Input Workspace",
    "Upload the source resume and paste the role description. The layout and styling below are presentation-only changes; the underlying workflow remains the same.",
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="panel-card">
            <p class="panel-title">Resume Source</p>
            <p class="panel-description">Upload a PDF version of your resume to start the extraction and tailoring pipeline.</p>
        """,
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Upload your resume PDF",
        type=["pdf"],
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown(
        """
        <div class="panel-card">
            <p class="panel-title">Target Role</p>
            <p class="panel-description">Paste the full job description so the system can adapt phrasing, emphasis, and ATS keywords.</p>
        """,
        unsafe_allow_html=True,
    )
    job_description = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="Copy and paste the complete job description from the posting.\n\nInclude the title, responsibilities, requirements, and preferred skills.",
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="download-row">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate = st.button("Generate Application Materials", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if generate:
    if uploaded_file is None or not job_description.strip():
        st.error("Please upload a resume PDF and provide a job description.")
        render_status_panel(
            "Missing required inputs",
            "Both the resume PDF and the target job description are required before generation can begin.",
            "warning",
        )
    else:
        temp_pdf_path = None

        try:
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text("Saving uploaded PDF...")
            progress_bar.progress(10)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_pdf_path = tmp_file.name

            status_text.text("Extracting text from resume PDF...")
            progress_bar.progress(25)

            resume_text = extract_text_from_pdf(temp_pdf_path)

            if not resume_text.strip():
                st.error("Could not extract text from the uploaded PDF.")
                st.stop()

            status_text.text("Running planning and drafting workflow...")
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
                "ats_score": 0.0,
                "ats_breakdown": {},
            }

            status_text.text("Generating tailored application materials...")
            progress_bar.progress(75)

            with st.spinner("Finalizing your application package..."):
                result = graph.invoke(initial_state)

            progress_bar.progress(100)
            status_text.text("Application materials generated successfully.")
            progress_bar.empty()
            status_text.empty()

            render_section_intro(
                "Results",
                "Review the generated strategy, tailored resume content, verification feedback, and ATS scoring before exporting the final files.",
            )

            with st.expander("Extracted Resume Text", expanded=False):
                st.text_area("Extracted Text", value=resume_text, height=300)

            with st.expander("AI Analysis Plan", expanded=True):
                st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                st.markdown(
                    """
                    <p class="panel-title">Strategic Approach</p>
                    <p class="panel-description">This section summarizes the workflow's planning rationale before writing the tailored assets.</p>
                    """,
                    unsafe_allow_html=True,
                )
                st.write(result.get("plan", []))
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.markdown(
                """
                <p class="panel-title">Tailored Resume Bullets</p>
                <p class="panel-description">Rewritten experience bullets aligned to the target role and phrased for stronger impact.</p>
                """,
                unsafe_allow_html=True,
            )

            bullets = result.get("rewritten_bullets", [])
            if bullets:
                for job_idx, job_bullets in enumerate(bullets, 1):
                    st.markdown(
                        f'<p class="experience-label">Experience {job_idx}</p>',
                        unsafe_allow_html=True,
                    )
                    for i, bullet in enumerate(job_bullets, 1):
                        st.markdown(
                            f'<div class="bullet-point"><strong>{job_idx}.{i}</strong> {bullet}</div>',
                            unsafe_allow_html=True,
                        )
            else:
                render_status_panel(
                    "No bullet output",
                    "The workflow did not return rewritten bullets. Review the uploaded resume and job description, then try again.",
                    "warning",
                )

            flattened_bullets = []
            for job_idx, job_bullets in enumerate(bullets, 1):
                flattened_bullets.append(f"Job Experience {job_idx}:")
                for i, bullet in enumerate(job_bullets, 1):
                    flattened_bullets.append(f"{job_idx}.{i}. {bullet}")
                flattened_bullets.append("")

            bullets_text = "\n".join(flattened_bullets)
            st.download_button(
                label="Download Resume Bullets",
                data=bullets_text,
                file_name="tailored_resume_bullets.txt",
                mime="text/plain",
                use_container_width=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.markdown(
                """
                <p class="panel-title">Generated Cover Letter</p>
                <p class="panel-description">A personalized draft based on the role context and resume content.</p>
                """,
                unsafe_allow_html=True,
            )
            cover_letter = result.get("cover_letter", "")
            st.text_area(
                "Your personalized cover letter:",
                value=cover_letter,
                height=300,
                disabled=True,
            )
            st.download_button(
                label="Download Cover Letter",
                data=cover_letter,
                file_name="generated_cover_letter.txt",
                mime="text/plain",
                use_container_width=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            final_resume_text = result.get("final_resume_text", "")

            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.markdown(
                """
                <p class="panel-title">Resume Export</p>
                <p class="panel-description">Download the structured DOCX resume and review the generated resume text draft when available.</p>
                """,
                unsafe_allow_html=True,
            )

            if result.get("structured_resume"):
                temp_docx = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
                temp_docx_path = temp_docx.name
                temp_docx.close()

                build_docx_resume(result["structured_resume"], temp_docx_path)

                with open(temp_docx_path, "rb") as f:
                    st.download_button(
                        label="Download Resume (DOCX)",
                        data=f,
                        file_name="tailored_resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                    )

            if final_resume_text:
                st.text_area(
                    "Final modified resume text:",
                    value=final_resume_text,
                    height=350,
                    disabled=True,
                )
                st.download_button(
                    label="Download Modified Resume",
                    data=final_resume_text,
                    file_name="modified_resume.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.markdown(
                """
                <p class="panel-title">Quality Verification</p>
                <p class="panel-description">A final pass to flag whether the generated application package meets the workflow's internal quality checks.</p>
                """,
                unsafe_allow_html=True,
            )
            if result.get("verification_passed", False):
                render_status_panel(
                    "Verification passed",
                    "The application materials cleared the current quality checks and are ready for final review and export.",
                    "success",
                )
            else:
                render_status_panel(
                    "Verification review suggested",
                    "Some improvements may still be useful based on the generated verification feedback below.",
                    "warning",
                )

            with st.expander("Verification Details"):
                st.write("Passed:", result.get("verification_passed", False))
                st.write("Feedback:", result.get("feedback", ""))
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.markdown(
                """
                <p class="panel-title">ATS Compatibility Score</p>
                <p class="panel-description">A concise dashboard view of keyword match, formatting readiness, and skills alignment.</p>
                """,
                unsafe_allow_html=True,
            )
            ats_score = result.get("ats_score", 0.0)
            ats_breakdown = result.get("ats_breakdown", {})

            if ats_score >= 80:
                render_status_panel(
                    f"ATS score: {ats_score}/100",
                    "Strong ATS readiness with good overall alignment to the target role.",
                    "success",
                )
            elif ats_score >= 60:
                render_status_panel(
                    f"ATS score: {ats_score}/100",
                    "Solid foundation with room to improve keyword coverage or formatting precision.",
                    "default",
                )
            else:
                render_status_panel(
                    f"ATS score: {ats_score}/100",
                    "The draft likely needs more keyword and structure refinement before submission.",
                    "warning",
                )

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <p class="metric-label">Keyword Match</p>
                        <p class="metric-value">{ats_breakdown.get('keyword_match', 0)}/100</p>
                        <p class="metric-copy">Measures how strongly the resume language reflects the posting's core terms.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <p class="metric-label">Formatting</p>
                        <p class="metric-value">{ats_breakdown.get('formatting', 0)}/100</p>
                        <p class="metric-copy">Tracks whether the output stays compatible with ATS-friendly formatting expectations.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <p class="metric-label">Skills Alignment</p>
                        <p class="metric-value">{ats_breakdown.get('skills_alignment', 0)}/100</p>
                        <p class="metric-copy">Assesses how well the listed capabilities map to the target role requirements.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            matched = ats_breakdown.get("matched_keywords", [])
            missing = ats_breakdown.get("missing_keywords", [])

            with st.expander("ATS Score Breakdown", expanded=True):
                if matched:
                    st.markdown("**Matched Keywords**")
                    st.markdown(
                        "<ul class='keyword-list'>"
                        + "".join(f"<li>{keyword}</li>" for keyword in matched[:5])
                        + "</ul>",
                        unsafe_allow_html=True,
                    )
                    if len(matched) > 5:
                        st.caption(f"and {len(matched) - 5} more matched keywords")

                if missing:
                    render_status_panel(
                        "Suggested keywords to consider",
                        "These keywords appear underrepresented in the current output and may improve ATS alignment when added appropriately.",
                        "warning",
                    )
                    st.markdown(
                        "<ul class='keyword-list'>"
                        + "".join(f"<li>{keyword}</li>" for keyword in missing[:10])
                        + "</ul>",
                        unsafe_allow_html=True,
                    )
                    if len(missing) > 10:
                        st.caption(f"and {len(missing) - 10} more potential keywords")

            render_status_panel(
                "Application package ready",
                "Review the generated content, make any final edits you want, and export the assets for submission.",
                "success",
            )
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred while processing your resume: {str(e)}")

        finally:
            if temp_pdf_path and os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)

st.markdown(
    """
    <div class="footer-shell">
        <p class="footer-title">Job Application Copilot</p>
        <p class="footer-copy">Built with Streamlit and LangGraph to produce cleaner, more targeted application materials.</p>
        <p class="footer-copy">Review each generated asset before submission and personalize the strongest role-specific details.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
