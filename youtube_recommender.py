import os
from langchain_community.tools import YouTubeSearchTool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class YouTubeRecommender:
    def __init__(self):
        # Use LangChain's wrapper for Gemini
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.2,
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
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
            response = self.model.invoke(prompt)
            keywords = response.content.strip().split(',')
            return [kw.strip() for kw in keywords if kw.strip()]
        except Exception as e:
            print(f"Keyword generation failed: {e}")
            return ["career development", "professional skills", "interview preparation", "resume tips", "workplace communication"]
    
    def search_videos(self, keywords):
        """Search YouTube for videos based on keywords"""
        recommendations = []
        
        for keyword in keywords[:5]:  # Limit to 5 searches
            try:
                search_query = f"{keyword} tutorial course"
                results = self.youtube_tool.run(search_query)
                
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
