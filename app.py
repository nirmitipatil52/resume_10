# app.py
import streamlit as st
import pdfplumber
from docx import Document
import pandas as pd
from resume_parser import *
from skill_detector import*
from ats_score import *
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
# PROFESSIONAL UI UPGRADE FOR YOUR AI RESUME ANALYZER



st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# -----------------------------
# PROFESSIONAL UI DESIGN
# -----------------------------

# =========================================
# PREMIUM UI DESIGN
# =========================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide",
    page_icon="🚀"
)

# ---------------- CSS ----------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #07111f,
        #0d1b2a,
        #10243a
    );
    color: white;
}

/* HERO SECTION */

.hero-box {
    background: rgba(255,255,255,0.05);
    border-radius: 25px;
    padding: 40px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 25px;
}

.hero-title {
    font-size: 55px;
    font-weight: 800;
    color: white;
}

.hero-subtitle {
    font-size: 22px;
    color: #c7d5e0;
    margin-top: 10px;
}

/* FEATURE CARDS */

.feature-card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
    transition: 0.3s;
}

.feature-card:hover {
    transform: scale(1.03);
    border: 1px solid #00c6ff;
    box-shadow: 0 0 20px rgba(0,198,255,0.3);
}

.feature-title {
    font-size: 28px;
    font-weight: bold;
    color: white;
    margin-top: 10px;
}

.feature-text {
    color: #c7d5e0;
    margin-top: 10px;
}

/* SECTION BOX */

.section-box {
    background: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 25px;
    margin-top: 30px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* BUTTON */

.stButton>button {
    width: 100%;
    background: linear-gradient(
        90deg,
        #00c6ff,
        #0072ff
    );
    color: white;
    border-radius: 15px;
    border: none;
    height: 55px;
    font-size: 18px;
    font-weight: bold;
}

.stButton>button:hover {
    transform: scale(1.02);
}

/* METRICS */

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------

st.markdown("""
<div class="hero-box">

<div class="hero-title">
🚀 AI Resume Analyzer
</div>

<div class="hero-subtitle">
Smart Career Intelligence & ATS Optimization Platform
</div>

</div>
""", unsafe_allow_html=True)

# ---------------- FEATURE CARDS ----------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h1>📄</h1>
        <div class="feature-title">ATS Analysis</div>
        <div class="feature-text">
            Analyze ATS compatibility score instantly.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h1>🧠</h1>
        <div class="feature-title">Skill Detection</div>
        <div class="feature-text">
            Detect technical and professional skills.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h1>🎯</h1>
        <div class="feature-title">Role Prediction</div>
        <div class="feature-text">
            Predict best matching career role.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- MAIN SECTION ----------------

st.markdown("""
<div class="section-box">
""", unsafe_allow_html=True)

st.markdown("## 📑 Resume Upload & Analysis")

# -----------------------------
# LOAD DATASET
# -----------------------------

dataset = pd.read_csv("notebook/AI_Resume_Analyzer_Dataset.csv")

# -----------------------------
# EXTRACT ALL SKILLS
# -----------------------------

all_skills = []

for skills in dataset['Required_Skills']:
    skill_list = skills.split(',')

    for skill in skill_list:
        all_skills.append(skill.strip().lower())

all_skills = list(set(all_skills))

# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------

def extract_text_from_pdf(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    return text

# -----------------------------
# DOCX TEXT EXTRACTION
# -----------------------------

def extract_text_from_docx(docx_file):

    doc = Document(docx_file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text

# -----------------------------
# SKILL DETECTION
# -----------------------------

def detect_skills(text):

    detected_skills = []

    text = text.lower()

    for skill in all_skills:

        if skill in text:
            detected_skills.append(skill)

    return detected_skills

# -----------------------------
# ATS SCORE
# -----------------------------

def calculate_ats_score(detected_skills, target_role):

    role_data = dataset[dataset['Role'] == target_role]

    if len(role_data) == 0:
        return 0, [], []

    required_skills = role_data.iloc[0]['Required_Skills']

    required_skills = [
        skill.strip().lower()
        for skill in required_skills.split(',')
    ]

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill in detected_skills:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    score = (len(matched_skills) / len(required_skills)) * 100

    return round(score, 2), matched_skills, missing_skills

# -----------------------------
# ROLE PREDICTION
# -----------------------------

def predict_role(detected_skills):

    best_role = None
    best_score = 0

    role_scores = []

    for index, row in dataset.iterrows():

        role = row['Role']

        required_skills = [
            skill.strip().lower()
            for skill in row['Required_Skills'].split(',')
        ]

        matched = 0

        for skill in required_skills:

            if skill in detected_skills:
                matched += 1

        score = (matched / len(required_skills)) * 100

        role_scores.append((role, score))

        if score > best_score:
            best_score = score
            best_role = role

    role_scores.sort(key=lambda x: x[1], reverse=True)

    return best_role, best_score, role_scores[:5]

# -----------------------------
# SUGGESTIONS ENGINE
# -----------------------------

def generate_suggestions(target_role, missing_skills):

    suggestions = []

    role_data = dataset[dataset['Role'] == target_role]

    if len(role_data) == 0:
        return suggestions

    row = role_data.iloc[0]

    for skill in missing_skills:
        suggestions.append(f"Add skill: {skill}")

    suggestions.append(
        f"Recommended Certification: {row['Certifications']}"
    )

    suggestions.append(
        f"Suggested Project: {row['Recommended_Projects']}"
    )

    suggestions.append(
        f"Resume Tip: {row['Resume_Tips']}"
    )

    return suggestions

# -----------------------------
# SECTION CHECKER
# -----------------------------

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

# -----------------------------
# FILE UPLOAD
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

# -----------------------------
# PROCESS RESUME
# -----------------------------

if uploaded_file is not None:

    file_name = uploaded_file.name

    # Extract text
    if file_name.endswith('.pdf'):
        text = extract_text_from_pdf(uploaded_file)

    elif file_name.endswith('.docx'):
        text = extract_text_from_docx(uploaded_file)

    else:
        st.error("Unsupported file type")
        st.stop()

    st.success("Resume Uploaded Successfully ✅")

    # Detect skills
    detected_skills = detect_skills(text)

    # Predict role
    best_role, best_score, top_roles = predict_role(detected_skills)

    # ATS Score
    ats_score, matched_skills, missing_skills = calculate_ats_score(
        detected_skills,
        best_role
    )

    # Suggestions
    suggestions = generate_suggestions(best_role, missing_skills)

    # Section Checker
    found_sections, missing_sections = check_resume_sections(text)

    # -----------------------------
    # DASHBOARD
    # -----------------------------

    st.header("📊 Resume Analysis Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("ATS Score", f"{ats_score}%")
    col2.metric("Best Role", best_role)
    col3.metric("Role Match", f"{best_score:.1f}%")

    # -----------------------------
    # SKILLS
    # -----------------------------

    st.subheader("🧠 Detected Skills")

    if detected_skills:
        st.success(", ".join(detected_skills))

    else:
        st.warning("No skills detected")

    # -----------------------------
    # MATCHED SKILLS
    # -----------------------------

    st.subheader("✅ Matched Skills")

    if matched_skills:
        st.write(matched_skills)

    # -----------------------------
    # MISSING SKILLS
    # -----------------------------

    st.subheader("❌ Missing Skills")

    if missing_skills:
        st.write(missing_skills)

    # -----------------------------
    # TOP ROLES
    # -----------------------------

    st.subheader("🏆 Top Matching Roles")

    top_roles_df = pd.DataFrame(top_roles, columns=['Role', 'Match Score'])

    st.dataframe(top_roles_df)

    # -----------------------------
    # RESUME SECTIONS
    # -----------------------------

    st.subheader("📑 Resume Section Analysis")

    st.success(f"Found Sections: {', '.join(found_sections)}")

    if missing_sections:
        st.error(f"Missing Sections: {', '.join(missing_sections)}")

    # -----------------------------
    # SUGGESTIONS
    # -----------------------------

    st.subheader("💡 AI Suggestions")

    for s in suggestions:
        st.write("-", s)

    # -----------------------------
    # RESUME TEXT
    # -----------------------------

    with st.expander("📄 View Extracted Resume Text"):
        st.write(text)
# -----------------------------
# FEATURE SELECTION
# -----------------------------

st.markdown("## 🚀 Features")

feature = st.radio(
    "Choose Analysis Type",
    ["ATS Analysis", "Skill Detection", "Role Prediction"],
    horizontal=True
)

uploaded_file = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf", "docx"]
)

# -----------------------------
# PROCESS RESUME
# -----------------------------

if uploaded_file is not None:

    # SAVE FILE TEMPORARILY
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # EXTRACT TEXT
    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file.name)

    else:
        text = extract_text_from_docx(uploaded_file.name)

    # DETECT SKILLS
    detected_skills = detect_skills(text)

    # -----------------------------
    # ATS ANALYSIS
    # -----------------------------

    if feature == "ATS Analysis":

        st.subheader("📊 ATS Analysis Result")

        target_role = st.selectbox(
            "Select Target Role",
            dataset['Role'].unique()
        )

        score, matched, missing = calculate_ats_score(
            detected_skills,
            target_role
        )

        st.metric("ATS Score", f"{score}%")

        st.success(f"✅ Matched Skills: {', '.join(matched)}")

        st.error(f"❌ Missing Skills: {', '.join(missing)}")

    # -----------------------------
    # SKILL DETECTION
    # -----------------------------

    elif feature == "Skill Detection":

        st.subheader("🧠 Detected Skills")

        if len(detected_skills) > 0:

            for skill in detected_skills:
                st.success(skill)

        else:
            st.warning("No skills detected")

    # -----------------------------
    # ROLE PREDICTION
    # -----------------------------

    elif feature == "Role Prediction":

        st.subheader("🎯 Predicted Career Role")

        role_scores = {}

        for role in dataset['Role'].unique():

            score, _, _ = calculate_ats_score(
                detected_skills,
                role
            )

            role_scores[role] = score

        best_role = max(role_scores, key=role_scores.get)

        st.success(f"✅ Best Matching Role: {best_role}")

        st.metric(
            "Match Score",
            f"{role_scores[best_role]}%"
        )
# -----------------------------
# FOOTER
# -----------------------------

st.markdown("---")
st.caption("🚀 AI Resume Analyzer & Career Intelligence Platform")
st.markdown("</div>", unsafe_allow_html=True)

