import streamlit as st
import os
from job_search import JobSearchEngine
from cover_letter import CoverLetterGenerator
from resume_analyzer import ResumeAnalyzer
from youtube_recommender import YouTubeRecommender
import PyPDF2
import re
import io

# Page configuration
st.set_page_config(
    page_title="AI Job Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'job_results' not in st.session_state:
    st.session_state.job_results = []
if 'resume_content' not in st.session_state:
    st.session_state.resume_content = ""
if 'selected_job' not in st.session_state:
    st.session_state.selected_job = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Job Search"

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        # Extract text from all pages
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def main():
    st.title("🤖 AI Job Search Assistant")
    st.markdown("---")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    
    # Use session state to track current page
    page_options = ["Job Search", "Resume Analyzer", "Cover Letter Generator", "YouTube Courses"]
    
    # Get the index of current page
    current_index = page_options.index(st.session_state.current_page) if st.session_state.current_page in page_options else 0
    
    page = st.sidebar.radio(
        "Choose a feature:",
        page_options,
        index=current_index
    )
    
    # Update current page in session state
    st.session_state.current_page = page
    
    # Resume upload section (common for all features)
    st.sidebar.markdown("### Upload Resume")
    uploaded_file = st.sidebar.file_uploader(
        "Upload your resume (PDF or TXT format)",
        type=['pdf', 'txt'],
        help="Upload your resume as a PDF or plain text file"
    )
    
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            with st.spinner("Reading PDF..."):
                # Extract text from PDF
                extracted_text = extract_text_from_pdf(uploaded_file)
                
                if extracted_text:
                    st.session_state.resume_content = extracted_text
                    st.sidebar.success("✅ Resume uploaded and processed successfully!")
                    
                    # Show preview of extracted text
                    with st.sidebar.expander("📄 Preview Extracted Text"):
                        preview_text = extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
                        st.text_area("", value=preview_text, height=150, disabled=True)
                else:
                    st.sidebar.error("❌ Failed to extract text from PDF. Please try again.")
        else:
            # Handle text file
            st.session_state.resume_content = str(uploaded_file.read(), "utf-8")
            st.sidebar.success("✅ Resume uploaded successfully!")
    
    # Main content based on selected page
    if page == "Job Search":
        job_search_page()
    elif page == "Resume Analyzer":
        resume_analyzer_page()
    elif page == "Cover Letter Generator":
        cover_letter_page()
    elif page == "YouTube Courses":
        youtube_courses_page()

def job_search_page():
    st.header("🔍 Job Search")
    
    if not st.session_state.resume_content:
        st.warning("Please upload your resume first using the sidebar.")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        location = st.text_input("Job Location", value="Remote", placeholder="e.g., Remote, New York, San Francisco")
    
    with col2:
        search_button = st.button("🔍 Search Jobs", type="primary")
    
    if search_button and location:
        with st.spinner("Searching for jobs... This may take a few moments."):
            try:
                job_engine = JobSearchEngine()
                st.session_state.job_results = job_engine.run_job_search(
                    st.session_state.resume_content, 
                    location
                )
                
                if st.session_state.job_results:
                    st.success(f"Found {len(st.session_state.job_results)} job opportunities!")
                else:
                    st.info("No job listings found. Try adjusting your search criteria.")
                    
            except Exception as e:
                st.error(f"An error occurred during job search: {str(e)}")
    
    # Display job results
    if st.session_state.job_results:
        st.markdown("### Job Results")
        
        for i, job in enumerate(st.session_state.job_results):
            with st.expander(f"🏢 {job.get('title', 'N/A')} at {job.get('company', 'N/A')}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Location:** {job.get('location', 'N/A')}")
                    st.write(f"**Why it's a good fit:** {job.get('relevance_reason', 'N/A')}")
                    if job.get('link', '#') != '#':
                        st.markdown(f"[View Job Posting]({job.get('link')})")
                
                with col2:
                    if st.button(f"📝 Generate Cover Letter", key=f"cover_letter_{i}"):
                        # Store the selected job and navigate to cover letter page
                        st.session_state.selected_job = job
                        st.session_state.current_page = "Cover Letter Generator"
                        st.rerun()

def resume_analyzer_page():
    st.header("📊 AI-Powered Resume Analyzer")
    st.markdown("Get comprehensive analysis from our AI career expert powered by Google Gemini")
    
    if not st.session_state.resume_content:
        st.warning("Please upload your resume first using the sidebar.")
        return
    
    # Optional target role input
    target_role = st.text_input(
        "Target Role (Optional)", 
        placeholder="e.g., Software Engineer, Marketing Manager",
        help="Specify your target role for more tailored analysis"
    )
    
    col1, col2 = st.columns([2, 1])
    with col1:
        analyze_button = st.button("🤖 Analyze with AI", type="primary", key="analyze_resume")
    with col2:
        detailed_recs = st.button("📋 Get Detailed Recommendations", key="detailed_recs")
    
    if analyze_button:
        with st.spinner("🤖 AI is analyzing your resume... This may take 30-60 seconds for thorough analysis."):
            try:
                analyzer = ResumeAnalyzer()
                analysis = analyzer.analyze_resume(st.session_state.resume_content)
                st.session_state.analysis_result = analysis
                
                # ATS Score with color coding
                score = analysis.get('ats_score', 0)
                score_color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                
                st.markdown(f"## {score_color} ATS Compatibility Score: {score}/100")
                
                # Score interpretation
                if score >= 90:
                    st.success("🎉 Exceptional! Your resume is highly optimized for ATS systems.")
                elif score >= 80:
                    st.success("✅ Great! Your resume should perform well in most ATS systems.")
                elif score >= 70:
                    st.warning("⚠️ Good foundation, but some improvements needed for better ATS performance.")
                elif score >= 60:
                    st.warning("⚠️ Moderate ATS compatibility. Several improvements recommended.")
                else:
                    st.error("❌ Low ATS compatibility. Significant improvements needed.")
                
                # Detailed score breakdown if available
                if analysis.get('score_breakdown'):
                    st.markdown("### Score Breakdown")
                    breakdown = analysis['score_breakdown']
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Formatting", f"{breakdown.get('formatting_score', 0)}/25")
                    with col2:
                        st.metric("Keywords", f"{breakdown.get('keyword_optimization', 0)}/25")
                    with col3:
                        st.metric("Content Quality", f"{breakdown.get('content_quality', 0)}/25")
                    with col4:
                        st.metric("ATS Compatibility", f"{breakdown.get('ats_compatibility', 0)}/25")
                
                # Key metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Keywords Found", analysis.get('keyword_count', 'N/A'))
                with col2:
                    st.metric("Resume Sections", analysis.get('section_count', 'N/A'))
                with col3:
                    if analysis.get('achievement_analysis'):
                        st.metric("Quantified Achievements", analysis['achievement_analysis'].get('quantified_achievements', 'N/A'))
                
                # Strengths
                if analysis.get('strengths'):
                    st.markdown("### ✅ Key Strengths")
                    for i, strength in enumerate(analysis['strengths'], 1):
                        st.success(f"**{i}.** {strength}")
                
                # Critical improvements
                if analysis.get('critical_improvements'):
                    st.markdown("### 🎯 Priority Improvements")
                    for i, improvement in enumerate(analysis['critical_improvements'], 1):
                        st.error(f"**{i}.** {improvement}")
                
                # Top 3 priorities
                if analysis.get('top_3_priorities'):
                    st.markdown("### 🚀 Top 3 Action Items")
                    for i, priority in enumerate(analysis['top_3_priorities'], 1):
                        st.info(f"**Priority {i}:** {priority}")
                
                # ATS Red Flags
                if analysis.get('ats_red_flags'):
                    st.markdown("### ⚠️ ATS Red Flags")
                    for flag in analysis['ats_red_flags']:
                        st.warning(f"🚩 {flag}")
                
                # Missing Keywords
                if analysis.get('missing_keywords'):
                    st.markdown("### 🔍 Recommended Keywords to Add")
                    keywords_text = ", ".join(analysis['missing_keywords'])
                    st.info(f"**Keywords:** {keywords_text}")
                    
                    if st.button("📋 Copy Keywords", key="copy_keywords"):
                        st.success("Keywords copied to clipboard! (Feature would work in deployed app)")
                
                # Overall Assessment
                if analysis.get('overall_assessment'):
                    st.markdown("### 📝 AI Expert Assessment")
                    st.markdown(f"> {analysis['overall_assessment']}")
                
                # Industry Alignment
                if analysis.get('industry_alignment'):
                    st.markdown("### 🎯 Industry Alignment")
                    st.info(analysis['industry_alignment'])
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.info("💡 Try uploading your resume again or check your API keys in .env file")
    
    # Detailed Recommendations
    if detailed_recs and st.session_state.resume_content:
        with st.spinner("🎯 Generating detailed improvement recommendations..."):
            try:
                analyzer = ResumeAnalyzer()
                recommendations = analyzer.get_detailed_recommendations(
                    st.session_state.resume_content, 
                    target_role if target_role else None
                )
                
                st.markdown("## 📋 Detailed Improvement Recommendations")
                
                # Immediate Actions
                if recommendations.get('immediate_actions'):
                    st.markdown("### ⚡ Immediate Actions")
                    for i, action in enumerate(recommendations['immediate_actions'], 1):
                        st.success(f"**{i}.** {action}")
                
                # Content Improvements
                if recommendations.get('content_improvements'):
                    st.markdown("### 📝 Content Improvements")
                    for improvement in recommendations['content_improvements']:
                        st.info(f"💡 {improvement}")
                
                # Keyword Strategy
                if recommendations.get('keyword_strategy'):
                    st.markdown("### 🔍 Keyword Strategy")
                    for strategy in recommendations['keyword_strategy']:
                        st.info(f"🎯 {strategy}")
                
                # Achievement Examples
                if recommendations.get('achievement_examples'):
                    st.markdown("### 🏆 Achievement Enhancement Examples")
                    for example in recommendations['achievement_examples']:
                        st.success(f"✨ {example}")
                
            except Exception as e:
                st.error(f"❌ Could not generate recommendations: {str(e)}")
    
    # Show previous analysis if available
    if 'analysis_result' in st.session_state and not analyze_button:
        st.info("💡 Previous analysis available. Click 'Analyze with AI' for a fresh analysis.")

def cover_letter_page():
    st.header("📝 Cover Letter Generator")
    
    if not st.session_state.resume_content:
        st.warning("Please upload your resume first using the sidebar.")
        return
    
    # Check if a job was selected from job search
    if st.session_state.selected_job:
        job = st.session_state.selected_job
        st.success(f"✅ Generating cover letter for: **{job.get('title')}** at **{job.get('company')}**")
        
        # Add option to clear selection
        if st.button("🔄 Clear Job Selection"):
            st.session_state.selected_job = None
            st.rerun()
    else:
        st.info("💡 You can also select a job from the Job Search page to auto-fill the details.")
    
    # Manual job input
    with st.form("cover_letter_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.text_input(
                "Job Title", 
                value=st.session_state.selected_job.get('title', '') if st.session_state.selected_job else '',
                placeholder="e.g., Software Engineer"
            )
            company_name = st.text_input(
                "Company Name", 
                value=st.session_state.selected_job.get('company', '') if st.session_state.selected_job else '',
                placeholder="e.g., Google"
            )
        
        with col2:
            hiring_manager = st.text_input(
                "Hiring Manager (Optional)", 
                placeholder="e.g., John Smith"
            )
            job_description = st.text_area(
                "Job Description (Optional)",
                placeholder="Paste the job description here for a more tailored cover letter...",
                height=100
            )
        
        submit_button = st.form_submit_button("📝 Generate Cover Letter", type="primary")
    
    if submit_button and job_title and company_name:
        with st.spinner("Crafting your personalized cover letter..."):
            try:
                generator = CoverLetterGenerator()
                cover_letter = generator.generate_cover_letter(
                    resume_content=st.session_state.resume_content,
                    job_title=job_title,
                    company_name=company_name,
                    hiring_manager=hiring_manager,
                    job_description=job_description
                )
                
                st.markdown("### Your Cover Letter")
                st.text_area("", value=cover_letter, height=400, disabled=True)
                
                # Download button
                st.download_button(
                    label="📥 Download Cover Letter",
                    data=cover_letter,
                    file_name=f"cover_letter_{company_name}_{job_title}.txt",
                    mime="text/plain"
                )
                
                # Clear the selected job after generating cover letter
                if st.session_state.selected_job:
                    st.session_state.selected_job = None
                
            except Exception as e:
                st.error(f"An error occurred while generating the cover letter: {str(e)}")

def youtube_courses_page():
    st.header("📺 YouTube Course Recommendations")
    st.markdown("Get personalized learning recommendations based on your resume")

    if not st.session_state.resume_content:
        st.warning("Please upload your resume first using the sidebar.")
        return

    if st.button("🔍 Get Course Recommendations", type="primary"):
        with st.spinner("Finding the best courses for you..."):
            try:
                recommender = YouTubeRecommender()
                results = recommender.get_recommendations(st.session_state.resume_content)

                st.success("Found personalized course recommendations!")

                # Show generated keywords
                st.markdown("### 🎯 Focus Areas")
                keywords_display = " • ".join(results['keywords'])
                st.info(f"**Learning Keywords:** {keywords_display}")

                st.markdown("### 📚 Recommended Courses")

                if not results['recommendations']:
                    st.info("No specific recommendations found. Try uploading a more detailed resume.")
                    return

                for item in results['recommendations']:
                    st.subheader(f"Courses for: {item['keyword'].title()}")



                    videos = []
                    
                    # Handle different possible formats
                    if isinstance(item['videos'], str):
                        # Try multiple regex patterns
                        patterns = [
                            r'\[(.*?)\]\((.*?)\)',  # Markdown links: [title](url)
                            r'Title:\s*(.*?)\s*URL:\s*(.*?)(?:\n|$)',  # Title: ... URL: ...
                            r'(.*?)\s*-\s*(https?://[^\s]+)',  # Title - URL
                            r'https?://[^\s]+',  # Just URLs
                        ]
                        
                        for pattern in patterns:
                            matches = re.findall(pattern, item['videos'], re.MULTILINE | re.DOTALL)
                            if matches:
                                if pattern == r'https?://[^\s]+':
                                    # Just URLs found, create generic titles
                                    videos = [(f"Video {i+1}", url) for i, url in enumerate(matches)]
                                else:
                                    videos = matches
                                break
                        
                        # If no regex worked, try splitting by lines and look for URLs
                        if not videos:
                            lines = item['videos'].split('\n')
                            for i, line in enumerate(lines):
                                line = line.strip()
                                if 'youtube.com' in line or 'youtu.be' in line:
                                    # Extract URL from line
                                    url_match = re.search(r'https?://[^\s]+', line)
                                    if url_match:
                                        url = url_match.group()
                                        # Try to extract title (everything before the URL)
                                        title = re.sub(r'https?://[^\s]+', '', line).strip()
                                        title = re.sub(r'^[-•*]\s*', '', title).strip()  # Remove bullet points
                                        if not title:
                                            title = f"Video {i+1}"
                                        videos.append((title, url))
                    
                    elif isinstance(item['videos'], list):
                        # If it's already a list, handle different list formats
                        for video in item['videos']:
                            if isinstance(video, dict):
                                title = video.get('title', video.get('name', 'Untitled Video'))
                                url = video.get('url', video.get('link', '#'))
                                videos.append((title, url))
                            elif isinstance(video, tuple) and len(video) >= 2:
                                videos.append((video[0], video[1]))
                            elif isinstance(video, str):
                                # String in list, try to parse
                                url_match = re.search(r'https?://[^\s]+', video)
                                if url_match:
                                    url = url_match.group()
                                    title = re.sub(r'https?://[^\s]+', '', video).strip()
                                    title = re.sub(r'^[-•*]\s*', '', title).strip()
                                    videos.append((title or "Video", url))
                    
                    if not videos:
                        st.warning("Could not parse video recommendations for this keyword.")
                        st.text(f"Raw data: {item['videos']}")
                        continue

                    # Display videos in a grid
                    if len(videos) == 1:
                        cols = st.columns(1)
                    elif len(videos) == 2:
                        cols = st.columns(2)
                    else:
                        cols = st.columns(min(3, len(videos)))  # Max 3 columns

                    for i, (title, url) in enumerate(videos):
                        col_idx = i % len(cols)
                        with cols[col_idx]:
                            try:
                                # Clean and validate URL
                                url = url.strip()
                                if not url.startswith(('http://', 'https://')):
                                    url = 'https://' + url
                                
                                # Extract video ID from URL to generate thumbnail
                                video_id = None
                                if "youtube.com/watch?v=" in url:
                                    video_id = url.split('v=')[1].split('&')[0]
                                elif "youtu.be/" in url:
                                    video_id = url.split('/')[-1].split('?')[0]
                                
                                if video_id:
                                    # Generate thumbnail URL
                                    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                                    
                                    # Display thumbnail and title
                                    st.image(thumbnail_url, use_container_width=True)
                                    st.markdown(f"**[{title}]({url})**")
                                else:
                                    # Fallback: just show the link without thumbnail
                                    st.markdown(f"📺 **[{title}]({url})**")

                            except Exception as e:
                                st.error(f"Failed to display video '{title}': {str(e)}")
                                # Fallback: simple link
                                st.markdown(f"📺 [{title}]({url})")

            except Exception as e:
                st.error(f"Error getting recommendations: {str(e)}")
                st.info("💡 Make sure your API keys are properly configured in .env file")
                
                # Additional debugging info
                import traceback
                with st.expander("🔍 Debug Information"):
                    st.text(traceback.format_exc())

if __name__ == "__main__":
    main()