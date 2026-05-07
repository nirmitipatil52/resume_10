import pandas as pd

# Load dataset
dataset = pd.read_csv("notebook/AI_Resume_Analyzer_Dataset.csv")

# Get all skills
all_skills = []

for skills in dataset['Required_Skills']:

    skill_list = skills.split(',')

    for skill in skill_list:
        all_skills.append(skill.strip().lower())

# Remove duplicates
all_skills = list(set(all_skills))


# Detect skills
def detect_skills(text):

    detected_skills = []

    text = text.lower()

    for skill in all_skills:

        if skill in text:
            detected_skills.append(skill)

    return detected_skills
