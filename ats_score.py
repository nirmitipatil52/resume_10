import pandas as pd

# Load dataset
dataset = pd.read_csv("notebook/AI_Resume_Analyzer_Dataset.csv")


def calculate_ats_score(detected_skills, target_role):

    # Get role data
    role_data = dataset[dataset['Role'] == target_role]

    if len(role_data) == 0:
        return 0, [], []

    # Get required skills
    required_skills = role_data.iloc[0]['Required_Skills']

    required_skills = [
        skill.strip().lower()
        for skill in required_skills.split(',')
    ]

    # Match skills
    matched_skills = []

    missing_skills = []

    for skill in required_skills:

        if skill in detected_skills:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    # Calculate score
    score = (len(matched_skills) / len(required_skills)) * 100

    return round(score, 2), matched_skills, missing_skills