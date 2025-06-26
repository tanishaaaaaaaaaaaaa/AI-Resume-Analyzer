
import streamlit as st
import spacy
from pdfminer.high_level import extract_text
import re
from time import sleep

# Load NLP Model
nlp = spacy.load("en_core_web_sm")

# Function to Extract Text from PDF
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

# Function to Extract Skills from Text
def extract_skills(text):
    skills_list = ["python", "java", "c++", "machine learning", "data analysis", "excel", "communication", "problem solving", "sql", "power bi", "tableau"]
    extracted_skills = []
    text = text.lower()
    for skill in skills_list:
        if skill in text:
            extracted_skills.append(skill)
    return extracted_skills

# Function to Clean Text
def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

# Function to Compare Resume with Job Description
def match_with_job_description(resume_text, job_description):
    resume_text = resume_text.lower()
    job_description = job_description.lower()
    matched_keywords = []

    for word in job_description.split():
        if word in resume_text and word not in matched_keywords:
            matched_keywords.append(word)
    
    match_percentage = (len(matched_keywords) / len(set(job_description.split()))) * 100
    return matched_keywords, round(match_percentage, 2)

# Function to Suggest Resume Improvements
def suggest_improvements(found_skills, all_skills):
    missing_skills = [skill for skill in all_skills if skill not in found_skills]
    return missing_skills

# Streamlit App UI
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

st.sidebar.title("AI Resume Analyzer")
st.sidebar.info("Upload your PDF resume to analyze your skills and match with a job description.")

st.title("\U0001F4BC Smart Resume Screening Tool")
st.write("This tool analyzes your resume, extracts key skills, compares it with a job description, and suggests improvements.")

uploaded_file = st.file_uploader("Choose your Resume (PDF only)", type="pdf")
job_description = st.text_area("Paste the Job Description to match with your resume")

if uploaded_file is not None:
    with st.spinner("Reading your resume..."):
        with open("temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.read())
        resume_text = extract_text_from_pdf("temp_resume.pdf")
        cleaned_text = clean_text(resume_text)
        sleep(1)

    st.success("Resume uploaded and processed!")
    
    st.subheader("\U0001F4DD Extracted Resume Text")
    with st.expander("Click to view resume text"):
        st.write(cleaned_text)
    
    with st.spinner("Analyzing your skills..."):
        skills = extract_skills(cleaned_text)
        sleep(1)

    st.subheader("\U0001F4AA Identified Skills")
    if skills:
        st.success("We found the following skills in your resume:")
        st.write(", ".join(skills))
        st.progress(min(len(skills) * 10, 100))
    else:
        st.warning("No relevant skills found. Consider adding more industry-recognized skills to your resume.")
    
    # Suggest Improvements
    all_skills_list = ["python", "java", "c++", "machine learning", "data analysis", "excel", "communication", "problem solving", "sql", "power bi", "tableau"]
    improvements = suggest_improvements(skills, all_skills_list)

    if improvements:
        st.subheader("\U0001F527 Suggested Improvements")
        st.info("Consider adding or highlighting these skills to enhance your resume:")
        st.write(", ".join(improvements))

    if job_description:
        with st.spinner("Matching resume with job description..."):
            matched_keywords, match_percentage = match_with_job_description(cleaned_text, job_description)
            sleep(1)
        
        st.subheader("\U0001F4CB Job Description Match Results")
        st.write(f"Match Percentage: **{match_percentage}%**")
        if matched_keywords:
            st.success("Matching keywords found:")
            st.write(", ".join(matched_keywords))
        else:
            st.warning("No significant match found. Consider tailoring your resume to the job description.")

    st.balloons()

st.sidebar.markdown("---")
st.sidebar.info("Developed with ❤️ using Streamlit & spaCy")
