import os
from langchain_community.tools import YouTubeSearchTool
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class YouTubeRecommender:
    def __init__(self):
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.youtube_tool = YouTubeSearchTool()
    
    def generate_keywords(self, resume_content):
        """Generate 5-7 keywords for YouTube search based on resume"""
        prompt = f"""
        Based on this resume, generate 5-7 keywords for searching educational content on YouTube.
        Focus on skills, technologies, career development, and learning opportunities.
        Return only the keywords separated by commas, no explanations.
        
        Resume: {resume_content[:2000]}
        
        Keywords:
        """
        
        try:
            response = self.model.generate_content(prompt)
            keywords = response.text.strip().split(',')
            return [kw.strip() for kw in keywords if kw.strip()]
        except Exception as e:
            # Fallback keywords
            return ["career development", "professional skills", "interview preparation", "resume tips", "workplace communication"]
    
    def search_videos(self, keywords):
        """Search YouTube for videos based on keywords"""
        recommendations = []
        
        for keyword in keywords[:5]:  # Limit to 5 searches to avoid rate limits
            try:
                search_query = f"{keyword} tutorial course"
                results = self.youtube_tool.run(search_query)
                
                # Parse results and add to recommendations
                if results:
                    recommendations.append({
                        'keyword': keyword,
                        'videos': results
                    })
            except Exception as e:
                print(f"Error searching for {keyword}: {e}")
                continue
        
        return recommendations
    
    def get_recommendations(self, resume_content):
        """Get YouTube course recommendations based on resume"""
        keywords = self.generate_keywords(resume_content)
        recommendations = self.search_videos(keywords)
        
        return {
            'keywords': keywords,
            'recommendations': recommendations
        }