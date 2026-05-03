"""
Frontend UI Components Module
File: frontend/components.py
Description: Clean, dark-adaptive UI components for AI PDF Summarizer
"""

import streamlit as st
from datetime import datetime


def render_header():
    """Render clean minimal header"""
    st.markdown("""
    <div class="app-header fade-in">
        <span class="label">⚡ AI-Powered · Groq API</span>
        <h1>PDF <span>Summarizer</span></h1>
        <p>Drop a document. Get the essence — fast, private, and accurate.</p>
    </div>
    """, unsafe_allow_html=True)


def render_features():
    """Render feature highlights in clean card row"""
    st.markdown("""
    <div class="feat-grid fade-in">
        <div class="feat-card">
            <span class="icon">🤖</span>
            <div class="title">Groq-Powered Models</div>
            <div class="desc">Sub-second inference with state-of-the-art LLMs</div>
        </div>
        <div class="feat-card">
            <span class="icon">🔒</span>
            <div class="title">Fully Private</div>
            <div class="desc">Your document never leaves your session</div>
        </div>
        <div class="feat-card">
            <span class="icon">⚡</span>
            <div class="title">5 Summary Modes</div>
            <div class="desc">Extractive, abstractive, bullets, Q&amp;A, and insights</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar(GroqClient):
    """Render clean sidebar with connection status and settings"""
    with st.sidebar:
        st.markdown("## PDF Summarizer")
        st.markdown("<div class='sidebar-label'>Connection</div>", unsafe_allow_html=True)

        if GroqClient.check_connection():
            st.markdown(
                '<div class="status-badge status-success">● Groq Connected</div>',
                unsafe_allow_html=True
            )
            models = GroqClient.list_models()

            if models:
                selected_model = st.selectbox("Model", models, label_visibility="collapsed")
                st.caption(f"{len(models)} model(s) available")
            else:
                st.warning("No models found")
                selected_model = st.text_input("Model name", value="llama2")
        else:
            st.markdown(
                '<div class="status-badge status-error">✕ Not Connected — Check API Key</div>',
                unsafe_allow_html=True
            )
            st.stop()

        st.markdown("<div class='sidebar-label'>Summary Type</div>", unsafe_allow_html=True)
        summary_type = st.radio(
            "Type",
            [
                "Extractive (Key Sentences)",
                "Abstractive (AI-Generated)",
                "Bullet Points",
                "Question-Based Analysis",
                "Key Insights",
            ],
            label_visibility="collapsed",
        )

        st.markdown("<div class='sidebar-label'>Length</div>", unsafe_allow_html=True)
        summary_length = st.select_slider(
            "Length",
            options=["short", "medium", "long"],
            value="medium",
            label_visibility="collapsed",
        )

        st.markdown("---")

        if st.button("Reset Session", use_container_width=True):
            st.rerun()

        st.markdown("<div class='sidebar-label'>Help</div>", unsafe_allow_html=True)
        with st.expander("How to use"):
            st.markdown("""
1. Upload your PDF
2. Pick a model & summary type
3. Hit **Generate Summary**
4. Download as TXT or PDF
            """)

        with st.expander("About models"):
            st.markdown("""
**llama-3.3-70b-versatile** — Best for summarization, great balance of speed & quality  
**llama-3.1-8b-instant** — Fastest, ideal for quick summaries  
**openai/gpt-oss-120b** — Most powerful, 120B parameters  
**openai/gpt-oss-20b** — Very fast, cost-efficient  
**meta-llama/llama-4-scout-17b-16e-instruct** — Latest Llama 4 from Meta  
            """)

        return selected_model, summary_type, summary_length


def render_file_info(uploaded_file, total_pages):
    """Render file info as metric cards"""
    name = uploaded_file.name if len(uploaded_file.name) <= 22 else uploaded_file.name[:20] + "…"
    size_kb = uploaded_file.size / 1024

    st.markdown(f"""
    <div class="metric-row fade-in">
        <div class="metric-card" style="flex:2">
            <div class="val" style="font-size:1.1rem;font-family:'DM Sans',sans-serif">{name}</div>
            <div class="lbl">File Name</div>
        </div>
        <div class="metric-card">
            <div class="val">{size_kb:.1f}</div>
            <div class="lbl">Kilobytes</div>
        </div>
        <div class="metric-card">
            <div class="val">{total_pages}</div>
            <div class="lbl">Pages</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_text_statistics(extracted_text):
    """Render extracted text stats"""
    words = len(extracted_text.split())
    chars = len(extracted_text)

    st.markdown(f"""
    <div class="metric-row fade-in">
        <div class="metric-card">
            <div class="val">{words:,}</div>
            <div class="lbl">Words</div>
        </div>
        <div class="metric-card">
            <div class="val">{chars:,}</div>
            <div class="lbl">Characters</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_processing_status(selected_model, summary_type, summary_length):
    """Render a minimal processing status indicator"""
    st.markdown(f"""
    <div class="processing-box fade-in">
        <strong>Processing with {selected_model}</strong>
        &nbsp;·&nbsp; {summary_type} &nbsp;·&nbsp; {summary_length.capitalize()} length
    </div>
    """, unsafe_allow_html=True)


def render_summary_statistics(stats, processing_time, selected_model):
    """Render summary result stats"""
    short_model = selected_model.split("/")[-1] if "/" in selected_model else selected_model
    short_model = short_model[:12] + "…" if len(short_model) > 12 else short_model

    st.markdown(f"""
    <div class="metric-row fade-in">
        <div class="metric-card">
            <div class="val">{stats['original_words']:,}</div>
            <div class="lbl">Original Words</div>
        </div>
        <div class="metric-card">
            <div class="val">{stats['summary_words']:,}</div>
            <div class="lbl">Summary Words</div>
        </div>
        <div class="metric-card">
            <div class="val">{stats['compression_ratio']:.1f}%</div>
            <div class="lbl">Compressed</div>
        </div>
        <div class="metric-card">
            <div class="val">{processing_time:.1f}s</div>
            <div class="lbl">Time</div>
        </div>
        <div class="metric-card">
            <div class="val" style="font-size:1rem;font-family:'DM Sans',sans-serif">{short_model}</div>
            <div class="lbl">Model</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_summary_display(summary, summary_type):
    """Render the summary in a clean styled container"""
    safe_summary = summary.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")

    st.markdown(f"""
    <div class="summary-wrap fade-in">
        <div class="s-head">{summary_type}</div>
        <div class="s-body">{safe_summary}</div>
    </div>
    """, unsafe_allow_html=True)


def render_download_section(summary, uploaded_file, summary_type, exporter):
    """Render download buttons"""
    st.markdown('<div class="section-title">Download</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    with col1:
        st.download_button(
            label="Download as TXT",
            data=summary,
            file_name=f"summary_{ts}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col2:
        pdf_bytes = exporter.create_pdf(summary, uploaded_file.name, summary_type)
        st.download_button(
            label="Download as PDF",
            data=pdf_bytes,
            file_name=f"summary_{ts}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


def render_footer():
    """Render minimal footer"""
    st.markdown("""
    <div class="app-footer">
        AI PDF Summarizer &nbsp;·&nbsp; Powered by <span>Groq API</span> &nbsp;·&nbsp; Built with Python & Streamlit
    </div>
    """, unsafe_allow_html=True)