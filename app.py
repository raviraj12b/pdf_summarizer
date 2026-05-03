"""
AI-Powered PDF Document Summarizer - Cloud-Based Version
File: app.py
Author: Academic Project
Description: Streamlit Cloud compatible version using Groq API
"""

import streamlit as st
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import backend modules (cloud-based)
from backend.groq_client import GroqClient
from backend.cloud_summarizer import CloudAISummarizer
from backend.pdf_extractor import PDFTextExtractor
from backend.exporter import SummaryExporter
from backend.utils import calculate_statistics

# Import frontend modules (if you have them)
try:
    from frontend import (
        load_custom_css,
        render_header,
        render_features,
        render_file_info,
        render_text_statistics,
        render_summary_statistics,
        render_summary_display,
        render_download_section,
        render_footer
    )
    HAS_FRONTEND = True
except ImportError:
    HAS_FRONTEND = False

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="AI PDF Summarizer Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SIMPLE FRONTEND FUNCTIONS (if frontend module not available)
# ============================================================================

def simple_render_header():
    """Simple header without custom CSS"""
    st.title("🚀 AI-Powered PDF Summarizer")
    st.markdown("### Transform PDFs into Concise Summaries with AI")
    st.markdown("---")

def simple_render_sidebar(llm_client):
    """Simple sidebar"""
    st.sidebar.header("⚙️ Configuration")
    
    # Check connection
    st.sidebar.markdown("### 🔌 Connection Status")
    if llm_client.check_connection():
        st.sidebar.success("✅ Cloud API Connected")
        models = llm_client.list_models()
        
        # Model selection
        st.sidebar.markdown("### 🤖 AI Model")
        selected_model = st.sidebar.selectbox(
            "Select Model",
            models,
            help="Choose your AI model"
        )
    else:
        st.sidebar.error("❌ API Not Connected")
        st.sidebar.info("Check your API key in secrets")
        st.stop()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📝 Summary Settings")
    
    # Summary type
    summary_type = st.sidebar.radio(
        "Summarization Type",
        [
            "🎯 Extractive",
            "✨ Abstractive",
            "📌 Bullet Points",
            "❓ Question-Based",
            "💡 Key Insights"
        ]
    )
    
    # Summary length
    summary_length = st.sidebar.select_slider(
        "Summary Length",
        options=["short", "medium", "long"],
        value="medium"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 About")
    st.sidebar.info(
        "This app uses **Groq API** (cloud-based) for fast, "
        "free AI-powered summarization. No local installation required!"
    )
    
    return selected_model, summary_type, summary_length

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application"""
    
    # Load custom CSS if available
    if HAS_FRONTEND:
        load_custom_css()
        render_header()
        render_features()
    else:
        simple_render_header()
    
    # Initialize API client
    try:
        llm_client = GroqClient()
    except ValueError as e:
        st.error(f"❌ {str(e)}")
        st.info(
            "**To fix this:**\n"
            "1. Get a free API key from https://console.groq.com\n"
            "2. In Streamlit Cloud: Go to App Settings → Secrets\n"
            "3. Add: `GROQ_API_KEY = \"your-key-here\"`\n\n"
            "**For local testing:**\n"
            "Create `.streamlit/secrets.toml` and add the same line."
        )
        st.stop()
    
    # Render sidebar
    if HAS_FRONTEND:
        from frontend import render_sidebar
        selected_model, summary_type, summary_length = render_sidebar(llm_client)
    else:
        selected_model, summary_type, summary_length = simple_render_sidebar(llm_client)
    
    st.markdown("---")
    
    # File upload
    st.markdown("## 📁 Upload Your PDF Document")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload your PDF document for AI-powered summarization"
    )
    
    if uploaded_file:
        # Extract text
        with st.spinner("📖 Extracting text from PDF..."):
            extractor = PDFTextExtractor()
            extracted_text, total_pages = extractor.extract_text_from_pdf(uploaded_file)
        
        # Display file info
        if HAS_FRONTEND:
            render_file_info(uploaded_file, total_pages)
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📄 File", uploaded_file.name[:20] + "...")
            with col2:
                st.metric("💾 Size", f"{uploaded_file.size / 1024:.1f} KB")
            with col3:
                st.metric("📑 Pages", total_pages)
        
        if extracted_text:
            # Text preview
            with st.expander("📄 View Extracted Text Preview"):
                st.text_area(
                    "",
                    extracted_text[:2000] + "...",
                    height=300,
                    disabled=True
                )
            
            # Statistics
            if HAS_FRONTEND:
                render_text_statistics(extracted_text)
            else:
                word_count = len(extracted_text.split())
                st.info(f"📊 Total Words: **{word_count:,}**")
            
            st.markdown("---")
            
            # Generate button
            if st.button(
                "🚀 Generate AI Summary",
                type="primary",
                use_container_width=True
            ):
                summarizer = CloudAISummarizer(llm_client)
                
                # Progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                start_time = time.time()
                
                try:
                    status_text.text(f"🔄 Sending to {selected_model}...")
                    progress_bar.progress(25)
                    
                    # Generate summary
                    if "Extractive" in summary_type:
                        summary = summarizer.summarize_extractive(
                            extracted_text,
                            selected_model,
                            summary_length
                        )
                    elif "Abstractive" in summary_type:
                        summary = summarizer.summarize_abstractive(
                            extracted_text,
                            selected_model,
                            summary_length
                        )
                    elif "Bullet" in summary_type:
                        summary = summarizer.summarize_bullet_points(
                            extracted_text,
                            selected_model
                        )
                    elif "Question" in summary_type:
                        summary = summarizer.summarize_with_questions(
                            extracted_text,
                            selected_model
                        )
                    else:  # Key Insights
                        summary = summarizer.get_key_insights(
                            extracted_text,
                            selected_model
                        )
                    
                    progress_bar.progress(75)
                    status_text.text("⚙️ Processing response...")
                    
                    if summary:
                        progress_bar.progress(100)
                        time.sleep(0.5)
                        progress_bar.empty()
                        status_text.empty()
                        
                        processing_time = time.time() - start_time
                        stats = calculate_statistics(extracted_text, summary)
                        
                        # Success
                        st.success(
                            f"✅ Summary Generated in {processing_time:.1f}s!"
                        )
                        
                        st.markdown("---")
                        
                        # Statistics
                        st.markdown("## 📊 Summary Statistics")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Original Words", f"{stats['original_words']:,}")
                        with col2:
                            st.metric("Summary Words", f"{stats['summary_words']:,}")
                        with col3:
                            st.metric("Compression", f"{stats['compression_ratio']:.1f}%")
                        with col4:
                            st.metric("Time", f"{processing_time:.1f}s")
                        
                        st.markdown("---")
                        
                        # Display summary
                        st.markdown("## 📝 AI-Generated Summary")
                        st.markdown(f"**Type:** {summary_type}")
                        st.info(summary)
                        
                        # Copy-friendly
                        with st.expander("📋 Copy-Friendly Text"):
                            st.text_area("", summary, height=300)
                        
                        st.markdown("---")
                        
                        # Download
                        st.markdown("## 💾 Download Summary")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.download_button(
                                label="📄 Download as TXT",
                                data=summary,
                                file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                        
                        with col2:
                            exporter = SummaryExporter()
                            pdf_bytes = exporter.create_pdf(
                                summary,
                                uploaded_file.name,
                                summary_type
                            )
                            st.download_button(
                                label="📑 Download as PDF",
                                data=pdf_bytes,
                                file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        
                        # Footer
                        st.markdown("---")
                        st.info(
                            f"🤖 Generated using **{selected_model}** | "
                            f"📅 {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
                        )
                    
                    else:
                        progress_bar.empty()
                        status_text.empty()
                        st.error("❌ Failed to generate summary")
                        st.info("💡 Try again or use a different model")
                
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Check your API key and try again")
        
        else:
            st.error("❌ Could not extract text from PDF")
            st.info("💡 Ensure PDF contains readable text")
    
    # Footer
    if HAS_FRONTEND:
        render_footer()
    else:
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: #666;'>"
            "<p>🎓 AI-Powered PDF Summarizer</p>"
            "<p>Powered by Groq API | Built with Streamlit</p>"
            "</div>",
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()
