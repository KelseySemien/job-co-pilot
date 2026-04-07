import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def tailor_resume(resume_text, job_description):
    """Tailor your resume for a specific job"""
    
    if not resume_text or not job_description:
        return "Please provide both resume and job description."
    
    prompt = f"""You are an expert resume writer. Tailor this resume for the job description below.

IMPORTANT RULES:
1. NEVER add false information
2. Keep all factual information (dates, companies, titles) exactly the same
3. Reorder and rephrase bullet points to highlight relevant experience
4. Use keywords from the job description naturally
5. Keep the same length

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide the tailored resume:"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional resume writer. Never invent or add false information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def generate_cover_letter(resume_text, job_description):
    """Generate a tailored cover letter"""
    
    prompt = f"""Write a professional cover letter for this job:

JOB: {job_description}

Based on this resume: {resume_text}

Requirements:
- 3-4 paragraphs
- Professional tone
- Mention specific skills from the resume
- Show enthusiasm for the role
- Keep it concise"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def calculate_match_score(resume_text, job_description):
    """Calculate a simple keyword match score"""
    
    # Common tech keywords (add more relevant to your field)
    keywords = [
        'python', 'machine learning', 'deep learning', 'tensorflow', 
        'pytorch', 'nlp', 'computer vision', 'sql', 'data analysis',
        'llm', 'langchain', 'streamlit', 'api', 'git', 'docker'
    ]
    
    job_lower = job_description.lower()
    resume_lower = resume_text.lower()
    
    matched = 0
    total = 0
    
    for keyword in keywords:
        if keyword in job_lower:
            total += 1
            if keyword in resume_lower:
                matched += 1
    
    if total == 0:
        return 50  # Default if no keywords found
    
    score = (matched / total) * 100
    return int(score)

# Test code (run this file directly to test)
if __name__ == "__main__":
    print("Testing Resume Tailor...")
    test_resume = "MS in AI student with Python and ML experience"
    test_job = "Looking for ML Engineer with Python skills"
    result = tailor_resume(test_resume, test_job)
    print("Success!" if "Error" not in result else "Check your API key")