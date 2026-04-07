import streamlit as st
from resume_tailor import tailor_resume, generate_cover_letter, calculate_match_score
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Job Co-pilot",
    page_icon="🎯",
    layout="wide"
)

# Title
st.title("🎯 AI Job Application Co-pilot")
st.markdown("*Your intelligent assistant for crafting tailored job applications*")

# Sidebar
with st.sidebar:
    st.header("📄 Your Resume")
    
    # Option 1: Upload file
    uploaded_file = st.file_uploader("Upload your resume (TXT file)", type=['txt'])
    
    # Option 2: Paste text
    resume_text = st.text_area(
        "Or paste your resume here:",
        height=200,
        placeholder="Paste your resume text here..."
    )
    
    if uploaded_file is not None:
        resume_text = uploaded_file.read().decode('utf-8')
        st.success("✅ Resume loaded from file!")
    
    # Sample resume button
    if st.button("📋 Load Sample Resume"):
        resume_text = """John Smith
Graduate Student in Artificial Intelligence

Education:
MS in Artificial Intelligence, University of Technology (Expected 2026)
- GPA: 3.8/4.0
- Relevant: Machine Learning, Deep Learning, NLP

Technical Skills:
Python, PyTorch, TensorFlow, SQL, Git, Docker, Streamlit

Projects:
- Resume Analyzer: Built LLM-based tool using LangChain
- Image Classifier: CNN with 92% accuracy
- Chatbot: Fine-tuned GPT model for customer service

Experience:
AI Research Assistant (2024-Present)
- Developed ML models for text classification
- Collaborated with team of 5 on research papers

Course Assistant (2023-2024)
- Taught Python programming to 30+ students"""
        st.rerun()

# Main area - two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Job Description")
    job_description = st.text_area(
        "Paste the job description here:",
        height=300,
        placeholder="Paste the full job description from LinkedIn, Indeed, etc..."
    )
    
    # Example job button
    if st.button("📋 Load Example Job"):
        job_description = """Machine Learning Engineer - AI Startup

We're seeking a Machine Learning Engineer with:
- Strong Python skills
- Experience with PyTorch or TensorFlow
- Knowledge of NLP and LLMs
- Ability to build and deploy ML models

Requirements:
- MS in CS/AI or equivalent
- 1+ years of ML experience
- Strong problem-solving skills"""
        st.rerun()

with col2:
    st.header("✨ Results")
    
    if st.button("🚀 Generate Tailored Application", type="primary"):
        if not job_description:
            st.warning("⚠️ Please paste a job description first!")
        elif not resume_text:
            st.warning("⚠️ Please provide your resume first!")
        else:
            with st.spinner("🤖 AI is tailoring your application..."):
                # Show match score
                score = calculate_match_score(resume_text, job_description)
                
                # Display score with color
                if score >= 70:
                    st.success(f"🎯 Match Score: {score}% - Excellent fit!")
                elif score >= 40:
                    st.warning(f"📊 Match Score: {score}% - Good potential")
                else:
                    st.info(f"📈 Match Score: {score}% - Consider highlighting transferable skills")
                
                # Generate tailored resume
                st.subheader("📄 Tailored Resume")
                tailored = tailor_resume(resume_text, job_description)
                st.text_area("Copy this tailored resume:", tailored, height=250, key="resume_output")
                
                # Generate cover letter
                st.subheader("✉️ Cover Letter")
                cover = generate_cover_letter(resume_text, job_description)
                st.text_area("Copy this cover letter:", cover, height=200, key="cover_output")
                
                # Save to file
                os.makedirs("output", exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                with open(f"output/tailored_resume_{timestamp}.txt", "w") as f:
                    f.write(tailored)
                with open(f"output/cover_letter_{timestamp}.txt", "w") as f:
                    f.write(cover)
                
                st.success(f"💾 Saved to output folder at {timestamp}")

# Instructions
with st.expander("💡 How to use this app"):
    st.markdown("""
    1. **Add your resume** (upload file or paste text)
    2. **Paste a job description** from any job board
    3. **Click Generate** to get tailored resume and cover letter
    4. **Copy the results** and use in your application
    
    **Pro Tips:**
    - The match score shows how well your skills align
    - Always review the AI's work before submitting
    - Save your best versions in the output folder
    """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit + OpenAI")