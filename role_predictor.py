import pandas as pd

# Load dataset
dataset = pd.read_csv("notebook/AI_Resume_Analyzer_Dataset.csv")


def predict_role(detected_skills):

    best_role = None

    best_score = 0

    role_scores = []

    # Check every role
    for index, row in dataset.iterrows():

        role = row['Role']

        required_skills = [
            skill.strip().lower()
            for skill in row['Required_Skills'].split(',')
        ]

        # Count matching skills
        matched = 0

        for skill in required_skills:

            if skill in detected_skills:
                matched += 1

        # Calculate match percentage
        score = (matched / len(required_skills)) * 100

        role_scores.append((role, score))

        # Best role
        if score > best_score:
            best_score = score
            best_role = role

    # Sort roles
    role_scores.sort(key=lambda x: x[1], reverse=True)

    return best_role, best_score, role_scores[:5]
