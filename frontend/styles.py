"""
Frontend Styling Module
File: frontend/styles.py
Description: Clean dark-adaptive CSS for AI PDF Summarizer
"""

import streamlit as st

def load_custom_css():
    """Load clean, dark-adaptive CSS styling"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');

    /* ── CSS Variables ── */
    :root {
        --bg-primary:      #0D0F12;
        --bg-secondary:    #13161B;
        --bg-card:         #1A1E26;
        --bg-card-hover:   #1F2430;
        --border:          #2A2F3D;
        --border-light:    #353C4E;

        --accent:          #4F8EF7;
        --accent-dim:      rgba(79, 142, 247, 0.15);
        --accent-glow:     rgba(79, 142, 247, 0.25);

        --success:         #34D399;
        --success-dim:     rgba(52, 211, 153, 0.12);
        --warning:         #FBBF24;
        --warning-dim:     rgba(251, 191, 36, 0.12);
        --danger:          #F87171;
        --danger-dim:      rgba(248, 113, 113, 0.12);

        --text-primary:    #F0F2F5;
        --text-secondary:  #8B93A7;
        --text-muted:      #545C6E;

        --radius-sm:  8px;
        --radius-md:  12px;
        --radius-lg:  16px;
        --radius-xl:  24px;

        --shadow-sm:  0 1px 3px rgba(0,0,0,0.4);
        --shadow-md:  0 4px 16px rgba(0,0,0,0.5);
        --shadow-lg:  0 8px 32px rgba(0,0,0,0.6);
        --shadow-accent: 0 0 24px rgba(79, 142, 247, 0.2);
    }

    /* Light-mode overrides */
    @media (prefers-color-scheme: light) {
        :root {
            --bg-primary:    #F4F6FA;
            --bg-secondary:  #EAEEF5;
            --bg-card:       #FFFFFF;
            --bg-card-hover: #F0F4FB;
            --border:        #D8DEE9;
            --border-light:  #C4CCDB;

            --text-primary:  #111827;
            --text-secondary:#4B5563;
            --text-muted:    #9CA3AF;

            --shadow-sm:  0 1px 3px rgba(0,0,0,0.08);
            --shadow-md:  0 4px 16px rgba(0,0,0,0.10);
            --shadow-lg:  0 8px 32px rgba(0,0,0,0.12);
            --shadow-accent: 0 0 24px rgba(79, 142, 247, 0.12);
        }
    }

    /* ── Global Reset ── */
    * { font-family: 'DM Sans', sans-serif; box-sizing: border-box; }
    html, body, .stApp {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-secondary); }
    ::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding: 2rem 2.5rem !important;
        max-width: 1100px !important;
    }

    /* ── Header ── */
    .app-header {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 0.4rem;
        padding: 2.5rem 0 2rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 2rem;
    }
    .app-header .label {
        font-family: 'Space Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--accent);
        background: var(--accent-dim);
        padding: 4px 12px;
        border-radius: 100px;
        border: 1px solid rgba(79,142,247,0.3);
    }
    .app-header h1 {
        font-size: 2.6rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.03em;
        margin: 0 !important;
        line-height: 1.1 !important;
    }
    .app-header h1 span { color: var(--accent); }
    .app-header p {
        color: var(--text-secondary);
        font-size: 1rem;
        font-weight: 400;
        margin: 0;
    }

    /* ── Feature Cards ── */
    .feat-grid { display: flex; gap: 1rem; margin: 1.5rem 0; }
    .feat-card {
        flex: 1;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.25rem 1.4rem;
        transition: border-color 0.2s, transform 0.2s;
    }
    .feat-card:hover {
        border-color: var(--accent);
        transform: translateY(-2px);
        box-shadow: var(--shadow-accent);
    }
    .feat-card .icon {
        font-size: 1.6rem;
        margin-bottom: 0.6rem;
        display: block;
    }
    .feat-card .title {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.3rem;
    }
    .feat-card .desc {
        font-size: 0.82rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }

    /* ── Metric Cards ── */
    .metric-row { display: flex; gap: 1rem; margin: 1rem 0; flex-wrap: wrap; }
    .metric-card {
        flex: 1;
        min-width: 120px;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.2rem 1rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: var(--accent);
        opacity: 0.7;
    }
    .metric-card .val {
        font-family: 'Space Mono', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
    }
    .metric-card .lbl {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-muted);
        margin-top: 0.4rem;
    }

    /* ── Status Badges ── */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: var(--radius-sm);
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.5rem 0;
    }
    .status-success {
        background: var(--success-dim);
        border: 1px solid rgba(52,211,153,0.3);
        color: var(--success);
    }
    .status-error {
        background: var(--danger-dim);
        border: 1px solid rgba(248,113,113,0.3);
        color: var(--danger);
    }
    .status-warning {
        background: var(--warning-dim);
        border: 1px solid rgba(251,191,36,0.3);
        color: var(--warning);
    }

    /* ── Processing Box ── */
    .processing-box {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent);
        border-radius: var(--radius-md);
        padding: 1rem 1.4rem;
        margin: 1rem 0;
        font-size: 0.88rem;
        color: var(--text-secondary);
    }
    .processing-box strong { color: var(--accent); font-weight: 600; }

    /* ── Summary Container ── */
    .summary-wrap {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-md);
    }
    .summary-wrap .s-head {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--accent);
        margin-bottom: 1.2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border);
    }
    .summary-wrap .s-body {
        font-size: 1rem;
        line-height: 1.85;
        color: var(--text-primary);
        white-space: pre-wrap;
    }

    /* ── File Upload ── */
    [data-testid="stFileUploadDropzone"] {
        background: var(--bg-card) !important;
        border: 1.5px dashed var(--border-light) !important;
        border-radius: var(--radius-lg) !important;
        transition: border-color 0.2s !important;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: var(--accent) !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text-primary) !important; }
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] p { color: var(--text-secondary) !important; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: var(--text-primary) !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
    }

    /* ── Sidebar section label ── */
    .sidebar-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: var(--text-muted);
        margin: 1.5rem 0 0.5rem;
        font-weight: 600;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: var(--accent) !important;
        color: #fff !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        padding: 0.65rem 1.5rem !important;
        transition: opacity 0.2s, transform 0.15s !important;
        box-shadow: 0 2px 8px rgba(79,142,247,0.3) !important;
    }
    .stButton > button:hover {
        opacity: 0.88 !important;
        transform: translateY(-1px) !important;
    }

    /* ── Download Buttons ── */
    .stDownloadButton > button {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: border-color 0.2s, background 0.2s !important;
    }
    .stDownloadButton > button:hover {
        border-color: var(--accent) !important;
        background: var(--accent-dim) !important;
        color: var(--accent) !important;
    }

    /* ── Selectbox / Radio / Slider ── */
    .stSelectbox > div > div,
    .stTextInput > div > div > input {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
    }
    .stRadio > div { gap: 0.4rem !important; }
    .stRadio label { color: var(--text-secondary) !important; font-size: 0.88rem !important; }

    /* ── Progress Bar ── */
    .stProgress > div > div > div {
        background: var(--accent) !important;
    }

    /* ── Alerts ── */
    .stAlert { border-radius: var(--radius-md) !important; border: none !important; }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-secondary) !important;
        font-size: 0.88rem !important;
    }

    /* ── Divider ── */
    hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

    /* ── Footer ── */
    .app-footer {
        text-align: center;
        padding: 2rem 0 1rem;
        margin-top: 2.5rem;
        border-top: 1px solid var(--border);
        color: var(--text-muted);
        font-size: 0.8rem;
    }
    .app-footer span { color: var(--accent); }

    /* ── Section Titles ── */
    .section-title {
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.01em;
        margin: 1.8rem 0 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
        margin-left: 0.5rem;
    }

    /* ── Fade-in Animation ── */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .fade-in { animation: fadeUp 0.35s ease forwards; }

    /* ── Responsive ── */
    @media (max-width: 768px) {
        .app-header h1 { font-size: 1.8rem !important; }
        .feat-grid { flex-direction: column; }
        .metric-row { flex-wrap: wrap; }
        .block-container { padding: 1rem 1.2rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)