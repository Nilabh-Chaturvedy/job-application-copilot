def build_resume_text(structured_resume: dict) -> str:
    lines = []

    summary = structured_resume.get("summary", "")
    if summary:
        lines.append("SUMMARY")
        lines.append(summary)
        lines.append("")

    experience = structured_resume.get("experience", [])
    if experience:
        lines.append("EXPERIENCE")
        for item in experience:
            header = f"{item.get('role', '')} | {item.get('company', '')}"
            lines.append(header)

            location = item.get("location", "")
            dates = item.get("dates", "")
            if location or dates:
                lines.append(f"{location} | {dates}".strip(" |"))

            for bullet in item.get("bullets", []):
                lines.append(f"- {bullet}")
            lines.append("")

    skills = structured_resume.get("skills", [])
    if skills:
        lines.append("SKILLS")
        lines.append(", ".join(skills))
        lines.append("")

    education = structured_resume.get("education", [])
    if education:
        lines.append("EDUCATION")
        for item in education:
            lines.append(
                f"{item.get('degree', '')} - {item.get('institution', '')} ({item.get('dates', '')})"
            )

    return "\n".join(lines).strip()