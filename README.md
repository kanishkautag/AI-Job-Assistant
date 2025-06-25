# 🚀 AI Job Assistant: Your Ultimate Career Co-Pilot 🚀

## Unlocking Your Next Opportunity with Intelligent Automation

Welcome to the **AI Job Assistant**, a powerful and intuitive Streamlit application designed to revolutionize your job search. Leveraging the advanced capabilities of AI, this tool acts as your personal career co-pilot, guiding you through job discovery, resume optimization, and cover letter generation, and even suggesting skill-building courses. Say goodbye to generic applications and hello to a tailored, efficient, and successful job hunt!

---

## ✨ Features at a Glance

This AI Job Assistant is packed with intelligent features to give you an edge in the competitive job market:

### 🔍 **Smart Job Search**
* **Personalized Job Matching:** Finds relevant job opportunities based on the skills and experience extracted from your resume.
* **Location-Aware Search:** Specify your preferred work location (e.g., "Remote", "New York", "San Francisco") to narrow down results.
* **Relevance Insights:** Understand *why* a job is a good fit for you with AI-driven relevance reasons.

### 📊 **AI-Powered Resume Analyzer**
* **Instant ATS Compatibility Score:** Get a score out of 100 indicating how well your resume will pass Applicant Tracking Systems.
* **Detailed Score Breakdown:** See performance across formatting, keywords, content quality, and overall ATS compatibility.
* **Key Strengths & Priority Improvements:** Quickly identify what you're doing well and what needs immediate attention.
* **ATS Red Flags:** Pinpoint common issues that might get your resume filtered out.
* **Recommended Keywords:** Discover crucial keywords missing from your resume to enhance visibility.
* **AI Expert Assessment:** Receive a comprehensive, expert-level review of your resume.
* **Detailed Improvement Recommendations:** Get actionable advice on content, keyword strategy, and how to quantify your achievements for maximum impact.

### 📝 **Intelligent Cover Letter Generator**
* **Effortless Creation:** Generate tailored cover letters in seconds, perfectly matched to specific job postings.
* **Resume-Driven Content:** Automatically incorporates your skills and experiences from your uploaded resume.
* **Job Description Integration:** (Optional) Paste job descriptions for hyper-personalized letters that resonate with hiring managers.
* **One-Click Download:** Easily download your generated cover letters in plain text format.

### 📺 **Personalized YouTube Course Recommendations**
* **Skill Gap Identification:** AI analyzes your resume to identify potential skill gaps or areas for professional growth.
* **Curated Learning Paths:** Get recommendations for relevant YouTube courses and tutorials to upskill or reskill.
* **Direct Links & Thumbnails:** Conveniently browse and access recommended video content with titles and thumbnails.

---

## 🛠️ How It Works

The AI Job Assistant is built with Streamlit for an interactive user interface and leverages powerful AI models (like Google Gemini) for its core functionalities.

1.  **Upload Your Resume:** Begin by uploading your resume (PDF or TXT) in the sidebar. This powers all other features.
2.  **Navigate Features:** Use the sidebar to switch between Job Search, Resume Analyzer, Cover Letter Generator, and YouTube Courses.
3.  **Input Details:** Provide minimal additional information (like job location or target role) as prompted by each feature.
4.  **Instant Insights & Generation:** Click the respective buttons to receive immediate analysis, job listings, generated content, or course recommendations.

---

## 🚀 Get Started (Local Setup)

To run this application on your local machine, follow these steps:

### Prerequisites

* Python 3.8+
* `pip` (Python package installer)
* Google API Key (for Gemini)
* YouTube Data API Key (if `YouTubeRecommender` uses it directly for searches, otherwise `google-generative-ai` handles it)

### 1. Clone the Repository

```bash
git clone <repository_url> # Replace with your actual repository URL
cd ai-job-assistant
