from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class CoverLetterGenerator:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.7)
    
    def generate_cover_letter(
        self, 
        resume_content: str, 
        job_title: str, 
        company_name: str,
        hiring_manager: Optional[str] = None,
        job_description: Optional[str] = None
    ) -> str:
        """Generate a personalized cover letter based on resume and job details."""
        
        # Prepare the greeting
        if hiring_manager:
            greeting = f"Dear {hiring_manager},"
        else:
            greeting = "Dear Hiring Manager,"
        
        # Prepare job description context
        job_desc_context = ""
        if job_description:
            job_desc_context = f"""
            Job Description:
            ---
            {job_description}
            ---
            """
        
        # Current date
        current_date = datetime.now().strftime("%B %d, %Y")
        
        cover_letter_prompt = f"""
        You are an expert career counselor and professional writer. Create a compelling, personalized cover letter that will make the candidate stand out.

        Requirements:
        - Write in a professional yet engaging tone
        - Keep it to 3-4 paragraphs (about 250-400 words)
        - Start with a strong opening that grabs attention
        - Highlight 2-3 most relevant qualifications from the resume
        - Show genuine interest in the company and role
        - Include specific examples of achievements when possible
        - End with a confident call to action
        - Make it personal and avoid generic templates

        Candidate's Resume:
        ---
        {resume_content}
        ---

        {job_desc_context}

        Job Details:
        - Position: {job_title}
        - Company: {company_name}
        - Date: {current_date}
        - Greeting: {greeting}

        Format the cover letter properly with:
        1. Date at the top
        2. Proper greeting
        3. Body paragraphs
        4. Professional closing (Sincerely, [Name from resume])

        Write a cover letter that tells a story and makes a connection between the candidate's background and this specific opportunity.
        """
        
        response = self.llm.invoke(cover_letter_prompt)
        return response.content.strip()
    
    def generate_multiple_versions(
        self, 
        resume_content: str, 
        job_title: str, 
        company_name: str,
        hiring_manager: Optional[str] = None,
        job_description: Optional[str] = None,
        num_versions: int = 3
    ) -> list:
        """Generate multiple versions of cover letters for A/B testing."""
        
        versions = []
        tones = ["professional and confident", "enthusiastic and energetic", "thoughtful and analytical"]
        
        for i in range(min(num_versions, len(tones))):
            tone = tones[i]
            
            # Prepare the greeting
            if hiring_manager:
                greeting = f"Dear {hiring_manager},"
            else:
                greeting = "Dear Hiring Manager,"
            
            # Prepare job description context
            job_desc_context = ""
            if job_description:
                job_desc_context = f"""
                Job Description:
                ---
                {job_description}
                ---
                """
            
            current_date = datetime.now().strftime("%B %d, %Y")
            
            version_prompt = f"""
            Create a {tone} cover letter for the following job application.
            
            Requirements:
            - Tone: {tone}
            - Length: 250-400 words
            - Highlight different aspects of the candidate's background
            - Make it unique from other versions
            
            Candidate's Resume:
            ---
            {resume_content}
            ---

            {job_desc_context}

            Job Details:
            - Position: {job_title}
            - Company: {company_name}
            - Date: {current_date}
            - Greeting: {greeting}

            Create a complete, professional cover letter.
            """
            
            response = self.llm.invoke(version_prompt)
            versions.append({
                'version': i + 1,
                'tone': tone,
                'content': response.content.strip()
            })
        
        return versions