from src.llm_client import client
from src.config import OPENAI_MODEL
import re

def ats_scorer_agent(state):
    if "ats_scoring" not in state["plan"]:
        state["ats_score"] = 0.0
        state["ats_breakdown"] = {}
        return state

    resume_text = state["final_resume_text"]
    jd_text = state["job_description"]

    # Extract keywords from JD
    jd_keywords = extract_keywords(jd_text)
    
    # Calculate keyword match score
    keyword_score = calculate_keyword_match(resume_text, jd_keywords)
    
    # Calculate formatting score
    formatting_score = calculate_formatting_score(resume_text)
    
    # Calculate skills alignment score
    skills_score = calculate_skills_alignment(resume_text, jd_text)
    
    # Overall score (weighted average)
    overall_score = (keyword_score * 0.4) + (formatting_score * 0.3) + (skills_score * 0.3)
    
    state["ats_score"] = round(overall_score, 1)
    state["ats_breakdown"] = {
        "keyword_match": round(keyword_score, 1),
        "formatting": round(formatting_score, 1),
        "skills_alignment": round(skills_score, 1),
        "matched_keywords": [k for k in jd_keywords if k.lower() in resume_text.lower()],
        "missing_keywords": [k for k in jd_keywords if k.lower() not in resume_text.lower()]
    }
    
    return state

def extract_keywords(text):
    """Extract potential keywords from job description"""
    # Common tech keywords and skills
    tech_keywords = [
        'python', 'sql', 'machine learning', 'data science', 'analytics', 'tableau', 'power bi',
        'azure', 'aws', 'gcp', 'spark', 'hadoop', 'tensorflow', 'pytorch', 'nlp', 'deep learning',
        'statistics','computer vision','r', 'excel', 'data visualization', 'etl', 'data engineering', 'big data',
        'ai', 'artificial intelligence', 'computer vision', 'natural language processing','genai','agenticai'
    ]
    
    found_keywords = []
    text_lower = text.lower()
    
    for keyword in tech_keywords:
        if keyword in text_lower:
            found_keywords.append(keyword.title())
    
    return found_keywords

def calculate_keyword_match(resume_text, jd_keywords):
    """Calculate percentage of JD keywords found in resume"""
    if not jd_keywords:
        return 100.0
    
    resume_lower = resume_text.lower()
    matched = sum(1 for keyword in jd_keywords if keyword.lower() in resume_lower)
    
    return (matched / len(jd_keywords)) * 100

def calculate_formatting_score(resume_text):
    """Score resume formatting for ATS compatibility"""
    score = 100
    
    # Check for bullet points
    if '•' not in resume_text and '-' not in resume_text:
        score -= 20
    
    # Check for standard sections
    sections = ['experience', 'education', 'skills']
    resume_lower = resume_text.lower()
    for section in sections:
        if section not in resume_lower:
            score -= 10
    
    # Check for contact information
    contact_indicators = ['@', 'linkedin', 'github', 'phone', 'email']
    has_contact = any(indicator in resume_lower for indicator in contact_indicators)
    if not has_contact:
        score -= 15
    
    return max(0, score)

def calculate_skills_alignment(resume_text, jd_text):
    """Calculate how well skills section aligns with JD requirements"""
    # Extract skills from resume
    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()
    
    # Look for skills section
    skills_match = re.search(r'skills?:?\s*(.*?)(?:\n\n|\n[A-Z]|$)', resume_lower, re.DOTALL)
    if not skills_match:
        return 50.0  # Default if no clear skills section
    
    skills_text = skills_match.group(1)
    skills = [s.strip() for s in re.split(r'[,;•\n-]', skills_text) if s.strip()]
    
    # Check how many skills appear in JD
    matched_skills = sum(1 for skill in skills if skill.lower() in jd_lower)
    
    if not skills:
        return 50.0
    
    return (matched_skills / len(skills)) * 100