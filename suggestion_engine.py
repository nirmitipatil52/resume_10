import pandas as pd

# Load dataset
dataset = pd.read_csv("notebook/AI_Resume_Analyzer_Dataset.csv")


def generate_suggestions(target_role, missing_skills):

    suggestions = []

    # Find role data
    role_data = dataset[dataset['Role'] == target_role]

    if len(role_data) == 0:
        return suggestions

    row = role_data.iloc[0]

    # Add missing skill suggestions
    for skill in missing_skills:

        suggestions.append(f"Add skill: {skill}")

    # Certifications
    suggestions.append(
        f"Recommended Certification: {row['Certifications']}"
    )

    # Projects
    suggestions.append(
        f"Suggested Project: {row['Recommended_Projects']}"
    )

    # Resume Tips
    suggestions.append(
        f"Resume Tip: {row['Resume_Tips']}"
    )

    return suggestions
