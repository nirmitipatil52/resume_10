def check_resume_sections(text):

    text = text.lower()

    required_sections = {
        "Education": ["education", "academic"],
        "Skills": ["skills", "technical skills"],
        "Projects": ["projects", "project"],
        "Experience": ["experience", "work experience"],
        "Certifications": ["certifications", "certificate"]
    }

    found_sections = []

    missing_sections = []

    # Check sections
    for section, keywords in required_sections.items():

        found = False

        for keyword in keywords:

            if keyword in text:
                found = True
                break

        if found:
            found_sections.append(section)

        else:
            missing_sections.append(section)

    return found_sections, missing_sections
