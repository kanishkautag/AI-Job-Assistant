import time
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSerperAPIWrapper

load_dotenv()

class JobSearchEngine:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)
        self.search_tool = GoogleSerperAPIWrapper()
    
    def extract_job_profiles(self, resume_content: str) -> List[str]:
        """Extract relevant job titles from resume content."""
        profile_prompt = f"""
        Analyze the following resume and extract 5-7 specific job titles this person is qualified for. 
        Return ONLY the job titles, each on a new line.
        Focus on roles that match their skills and experience level.

        Resume:
        ---
        {resume_content}
        ---
        """
        
        profile_response = self.llm.invoke(profile_prompt)
        job_profiles = [line.strip() for line in profile_response.content.strip().split("\n") if line.strip()]
        
        if not job_profiles:
            raise ValueError("Could not extract job profiles from resume.")
        
        return job_profiles
    
    def search_jobs_online(self, job_profiles: List[str], location: str) -> List[Dict[str, Any]]:
        """Search for jobs online based on job profiles and location."""
        all_raw_results = []
        queries = [f'"{profile}" jobs in {location}' for profile in job_profiles]
        
        for query in queries:
            try:
                results_list = self.search_tool.results(query, num_results=5)
                all_raw_results.extend(results_list.get("organic", []))
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"Warning: Could not execute query '{query}'. Error: {e}")
                continue
        
        return all_raw_results
    
    def structure_results(self, raw_results: List[Dict], resume_content: str) -> List[Dict[str, Any]]:
        """Structure raw search results into formatted job postings."""
        if not raw_results:
            return []
        
        structure_prompt = f"""
        You are an expert hiring assistant. Analyze the provided list of raw Google search results and a user's resume to identify valid job postings.

        From the results, extract up to 10 relevant job postings. Return your findings as a JSON object with a single key "jobs" which contains a list of objects. Each object should have the following keys: "title", "company", "location", "link", "relevance_reason".

        Only include results that are clearly job postings (not career advice articles, resume tips, etc.).
        Make the relevance_reason specific and personalized based on the resume.

        Resume for Context:
        ---
        {resume_content}
        ---

        Raw Search Results (JSON format):
        ---
        {json.dumps(raw_results, indent=2)}
        ---
        """
        
        structured_response = self.llm.invoke(structure_prompt)
        
        try:
            cleaned_response = structured_response.content.strip().replace("```json", "").replace("```", "")
            structured_data = json.loads(cleaned_response)
            return structured_data.get("jobs", [])
        except json.JSONDecodeError:
            print("Error: Failed to decode the structured response from the AI.")
            return []
    
    def run_job_search(self, resume_content: str, location: str) -> List[Dict[str, Any]]:
        """Main method to run the complete job search process."""
        try:
            # Step 1: Extract job profiles
            job_profiles = self.extract_job_profiles(resume_content)
            print(f"Found profiles: {', '.join(job_profiles)}")
            
            # Step 2: Search for jobs online
            raw_results = self.search_jobs_online(job_profiles, location)
            
            if not raw_results:
                print("No search results found.")
                return []
            
            # Step 3: Structure results
            structured_jobs = self.structure_results(raw_results, resume_content)
            
            return structured_jobs
            
        except Exception as e:
            print(f"Error in job search: {e}")
            raise e