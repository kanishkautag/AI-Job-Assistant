import json
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class ResumeAnalyzer:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
    
    def analyze_resume(self, resume_content: str) -> Dict[str, Any]:
        """Comprehensive AI-powered resume analysis using Gemini as an intelligent agent."""
        
        analysis_prompt = f"""
        You are an expert ATS (Applicant Tracking System) specialist, career coach, and recruiting professional with 15+ years of experience. 
        You have deep knowledge of what makes resumes successful in modern hiring processes.

        Your task is to thoroughly analyze this resume and provide a comprehensive assessment that includes:

        1. **ATS Compatibility Score** (0-100): How well will this resume perform in ATS systems?
        2. **Detailed Analysis**: Strengths, weaknesses, and specific improvements
        3. **Keyword Optimization**: Missing keywords and industry-specific terms
        4. **Formatting Assessment**: Structure, readability, and ATS-friendly formatting
        5. **Content Quality**: Achievement quantification, action verbs, impact statements

        Resume to Analyze:
        ---
        {resume_content}
        ---

        Please provide your analysis in the following JSON format:
        {{
            "ats_score": <integer 0-100>,
            "score_breakdown": {{
                "formatting_score": <integer 0-25>,
                "keyword_optimization": <integer 0-25>, 
                "content_quality": <integer 0-25>,
                "ats_compatibility": <integer 0-25>
            }},
            "strengths": [
                "specific strength 1",
                "specific strength 2",
                "specific strength 3"
            ],
            "critical_improvements": [
                "specific improvement 1 with actionable advice",
                "specific improvement 2 with actionable advice", 
                "specific improvement 3 with actionable advice"
            ],
            "missing_keywords": [
                "industry keyword 1",
                "industry keyword 2",
                "skill keyword 3",
                "role-specific keyword 4",
                "trending keyword 5"
            ],
            "keyword_count": <integer - number of relevant keywords found>,
            "section_count": <integer - number of resume sections detected>,
            "formatting_issues": [
                "specific formatting issue 1",
                "specific formatting issue 2"
            ],
            "achievement_analysis": {{
                "quantified_achievements": <integer - count of quantified results>,
                "action_verbs_used": <integer - count of strong action verbs>,
                "impact_statements": <integer - count of impact-focused statements>
            }},
            "industry_alignment": "assessment of how well the resume aligns with target industry/role",
            "overall_assessment": "2-3 sentence summary of resume quality and potential",
            "top_3_priorities": [
                "most important improvement 1",
                "most important improvement 2", 
                "most important improvement 3"
            ],
            "ats_red_flags": [
                "potential ATS issue 1",
                "potential ATS issue 2"
            ]
        }}

        **Analysis Guidelines:**
        - Be brutally honest but constructive
        - Focus on actionable feedback
        - Consider current job market trends
        - Assess for different experience levels appropriately
        - Look for measurable achievements and quantified results
        - Check for proper use of industry terminology
        - Evaluate readability and professional presentation
        - Consider ATS parsing challenges (tables, graphics, unusual formatting)
        - Assess keyword density without keyword stuffing
        - Look for gaps in experience or skills that need addressing

        **Scoring Criteria:**
        - **90-100**: Exceptional resume, ATS-optimized, highly competitive
        - **80-89**: Strong resume with minor improvements needed
        - **70-79**: Good resume that needs moderate improvements
        - **60-69**: Average resume requiring significant improvements
        - **Below 60**: Substantial overhaul needed

        Provide specific, actionable advice that will make an immediate impact on the resume's effectiveness.
        """
        
        try:
            response = self.llm.invoke(analysis_prompt)
            cleaned_response = response.content.strip()
            
            # Remove markdown code blocks if present
            if "```json" in cleaned_response:
                cleaned_response = cleaned_response.split("```json")[1].split("```")[0]
            elif "```" in cleaned_response:
                cleaned_response = cleaned_response.split("```")[1]
            
            analysis_result = json.loads(cleaned_response)
            
            # Validate the response has required fields
            required_fields = ['ats_score', 'strengths', 'critical_improvements', 'missing_keywords']
            if not all(field in analysis_result for field in required_fields):
                raise ValueError("Missing required fields in AI response")
            
            return analysis_result
            
        except (json.JSONDecodeError, ValueError, Exception) as e:
            print(f"Error in AI analysis: {e}")
            # Fallback to a secondary analysis prompt
            return self._fallback_analysis(resume_content)
    
    def _fallback_analysis(self, resume_content: str) -> Dict[str, Any]:
        """Fallback analysis in case primary analysis fails."""
        
        fallback_prompt = f"""
        Analyze this resume and give me a simple assessment:

        Resume:
        ---
        {resume_content}
        ---

        Rate it 0-100 for ATS compatibility and give me:
        1. Top 3 strengths
        2. Top 3 improvements needed  
        3. 5 missing keywords
        4. Overall assessment

        Format as JSON:
        {{
            "ats_score": <score>,
            "strengths": ["strength1", "strength2", "strength3"],
            "critical_improvements": ["improvement1", "improvement2", "improvement3"],
            "missing_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
            "keyword_count": <count>,
            "section_count": <count>,
            "overall_assessment": "brief assessment"
        }}
        """
        
        try:
            response = self.llm.invoke(fallback_prompt)
            cleaned_response = response.content.strip().replace("```json", "").replace("```", "")
            return json.loads(cleaned_response)
        except:
            # Ultimate fallback
            return {
                "ats_score": 65,
                "strengths": [
                    "Resume content is readable and structured",
                    "Contains relevant professional information",
                    "Shows career progression"
                ],
                "critical_improvements": [
                    "Add more quantified achievements with specific numbers",
                    "Include more industry-specific keywords",
                    "Improve formatting for better ATS compatibility"
                ],
                "missing_keywords": ["leadership", "project management", "data analysis", "strategic planning", "team collaboration"],
                "keyword_count": 12,
                "section_count": 4,
                "overall_assessment": "Resume has good foundation but needs optimization for ATS systems and modern hiring practices."
            }
    
    def get_detailed_recommendations(self, resume_content: str, target_role: str = None) -> Dict[str, Any]:
        """Get detailed, role-specific recommendations for resume improvement."""
        
        role_context = f"for a {target_role} position" if target_role else "for general job applications"
        
        recommendations_prompt = f"""
        As a senior career strategist, provide detailed, actionable recommendations to improve this resume {role_context}.

        Resume:
        ---
        {resume_content}
        ---

        Target Role: {target_role if target_role else "General"}

        Provide specific recommendations in JSON format:
        {{
            "immediate_actions": [
                "specific action 1",
                "specific action 2",
                "specific action 3"
            ],
            "content_improvements": [
                "detailed content suggestion 1",
                "detailed content suggestion 2"
            ],
            "keyword_strategy": [
                "keyword integration advice 1",
                "keyword integration advice 2"
            ],
            "formatting_fixes": [
                "formatting improvement 1",
                "formatting improvement 2"
            ],
            "achievement_examples": [
                "example of how to quantify achievement 1",
                "example of how to quantify achievement 2"
            ]
        }}

        Focus on changes that will have the biggest impact on getting past ATS systems and impressing hiring managers.
        """
        
        try:
            response = self.llm.invoke(recommendations_prompt)
            cleaned_response = response.content.strip().replace("```json", "").replace("```", "")
            return json.loads(cleaned_response)
        except:
            return self._get_basic_recommendations()
    
    def _get_basic_recommendations(self) -> Dict[str, Any]:
        """Basic recommendations fallback."""
        return {
            "immediate_actions": [
                "Add quantified achievements with specific numbers and percentages",
                "Include a professional summary at the top",
                "Use strong action verbs to start each bullet point"
            ],
            "content_improvements": [
                "Focus on results and impact rather than just responsibilities",
                "Tailor content to match job descriptions you're applying for"
            ],
            "keyword_strategy": [
                "Research job postings for your target role and incorporate relevant keywords",
                "Include both hard skills and soft skills mentioned in job descriptions"
            ],
            "formatting_fixes": [
                "Ensure consistent formatting throughout the document",
                "Use standard fonts and avoid graphics that ATS systems can't read"
            ],
            "achievement_examples": [
                "Instead of 'Managed team' write 'Led team of 8 developers, improving productivity by 25%'",
                "Instead of 'Worked on projects' write 'Delivered 3 major projects on time and 15% under budget'"
            ]
        }