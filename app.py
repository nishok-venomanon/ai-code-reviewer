import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Resume Reviewer", layout="centered")
st.title("📄 AI Resume Reviewer")

# Upload resume
resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# Optional job description
job_description = st.text_area("Paste the job description (optional)", height=200)

if st.button("Analyze"):
    if not resume_file:
        st.warning("Please upload your resume.")
    else:
        # Extract text from PDF
        reader = PdfReader(resume_file)
        resume_text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

        # Build prompt
        prompt = f"""
You are a career coach and resume expert. Analyze the following resume and provide:
1. Summary of strengths
2. Suggestions for improvement
3. ATS keyword gaps
{f"4. Match score and relevance for the job description below:\n{job_description}" if job_description else ""}

Resume:
{resume_text}
"""

        # Call OpenAI
        try:
            with st.spinner("Analyzing..."):
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful career coach."},
                        {"role": "user", "content": prompt}
                    ]
                )
                analysis = response.choices[0].message.content
                st.subheader("🧠 GPT Analysis")
                st.markdown(analysis)
        except Exception as e:
            st.error(f"Error: {e}")
