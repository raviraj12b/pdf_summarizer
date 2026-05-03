# AI PDF Summarizer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41.0-red)
![Groq](https://img.shields.io/badge/Groq-API-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Transform lengthy PDF documents into concise, AI-generated summaries**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Deployment](#-deployment-on-streamlit-cloud) • [Contributing](#-contributing)

</div>

---

## Overview

AI PDF Summarizer is a cloud-based application that leverages Large Language Models (LLMs) to automatically generate intelligent summaries from PDF documents. Built with Streamlit and powered by Groq's ultra-fast inference engine, it offers multiple summarization strategies to suit different needs.

### Key Highlights

- **Lightning Fast** — Powered by Groq's LPU inference engine
- **Multiple AI Models** — Choose from Llama 3.3 70B, GPT-OSS 120B, Llama 4, and more
- **5 Summarization Strategies** — Extractive, Abstractive, Bullet Points, Question-Based, and Key Insights
- **Cloud-Based** — No local AI model installation required
- **Export Options** — Download summaries as TXT or PDF
- **Free to Use** — Runs on Groq's free API tier

---

## Features

### AI-Powered Summarization
- **Extractive** — Selects and combines key sentences from the original text
- **Abstractive** — Generates a new, concise summary in the model's own words
- **Bullet Points** — Organized list of the most important information
- **Question-Based Analysis** — Answers critical questions about the document
- **Key Insights** — Extracts top takeaways and actionable implications

### Analytics
- Real-time word count and character statistics
- Compression ratio calculation
- Processing time tracking

### Export
- Download as plain TXT (preserves all content)
- Export as formatted PDF (Unicode-safe, built with FPDF2)

### UI
- Clean dark-adaptive interface (respects system dark/light mode)
- Minimal sidebar with clear section labels
- Responsive layout

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit 1.41.0 |
| AI Engine | Groq API |
| PDF Processing | PyPDF2 3.0.1 |
| PDF Export | FPDF2 2.8.1 |
| Language | Python 3.8+ |

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key — free from [console.groq.com](https://console.groq.com)

### Step 1 — Clone the repository
```bash
git clone https://github.com/yourusername/ai-pdf-summarizer.git
cd ai-pdf-summarizer
```

### Step 2 — Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Add your API key

Create `.streamlit/secrets.toml` in the project root:

```toml
GROQ_API_KEY = "your-groq-api-key-here"
```

**Getting a free Groq API key:**
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Go to API Keys → Generate new key
4. Paste it into `secrets.toml`

> **Important:** Never commit `secrets.toml` to GitHub. It is already listed in `.gitignore`.

### Step 5 — Run the app
```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## Usage

### Basic Workflow

1. **Upload a PDF** — click the file uploader and select a PDF
2. **Configure settings** in the sidebar:
   - Select an AI model
   - Choose a summarization type
   - Set summary length (short / medium / long)
3. **Generate** — click the Generate Summary button
4. **Download** — save as TXT or PDF

### Summarization Types

| Type | Description | Best For |
|------|-------------|----------|
| Extractive | Key sentences pulled from the original | Academic papers, preserving exact wording |
| Abstractive | New summary written by the AI | General use, readable output |
| Bullet Points | Organized list format | Presentations, quick scanning |
| Question-Based | Answers key questions about the document | Research, analysis |
| Key Insights | Top takeaways and implications | Executive summaries, decisions |

---

## Project Structure

```
ai-pdf-summarizer/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .gitignore                # Git ignore rules
│
├── .streamlit/
│   ├── config.toml           # App theme and settings (committed)
│   └── secrets.toml          # API keys — DO NOT commit
│
├── backend/
│   ├── __init__.py
│   ├── groq_client.py        # Groq API client
│   ├── cloud_summarizer.py   # Summarization logic
│   ├── pdf_extractor.py      # PDF text extraction
│   ├── exporter.py           # TXT and PDF export
│   └── utils.py              # Utility functions
│
└── frontend/
    ├── __init__.py
    ├── components.py         # UI components
    └── styles.py             # Custom CSS
```

---

## Deployment on Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app" → select your repo → set main file to `app.py`

3. **Add secrets**
   - In the Streamlit Cloud dashboard → App Settings → Secrets
   - Add:
     ```toml
     GROQ_API_KEY = "your-groq-api-key"
     ```

4. Click **Deploy**

---

## Available Models

| Model ID | Speed | Best For |
|----------|-------|----------|
| `llama-3.3-70b-versatile` | 280 T/s | Best quality, recommended default |
| `llama-3.1-8b-instant` | 560 T/s | Fast summarization, short docs |
| `openai/gpt-oss-120b` | 500 T/s | Most powerful, complex documents |
| `openai/gpt-oss-20b` | 1000 T/s | Fastest, cost-efficient |
| `meta-llama/llama-4-scout-17b-16e-instruct` | 750 T/s | Latest Llama 4, great all-rounder |

All models use Groq's free tier and support a 131K token context window.

---

## Performance

- **Processing time** — typically 3–15 seconds per document
- **Recommended PDF size** — up to 10MB
- **Context limit** — ~12,000 characters sent per request (long docs are truncated)
- **Compression ratio** — typically 70–95% reduction

---

## Troubleshooting

**Groq not connected**
```
❌ Groq API Not Connected
```
Check that `GROQ_API_KEY` is set correctly in `.streamlit/secrets.toml` or Streamlit Cloud secrets.

---

**Model decommissioned**
```
❌ The model 'llama3-70b-8192' has been decommissioned
```
Update to `llama-3.3-70b-versatile`. All current model IDs are listed in the Available Models table above.

---

**PDF font error**
```
❌ Character at index N is outside the range supported by the font
```
Fixed in the current version. The PDF exporter strips all emoji and non-latin-1 characters before rendering.

---

**PDF export crashes**
```
❌ Not enough horizontal space to render a single character
```
Fixed in the current version. The exporter now uses explicit page margins and is fully compatible with FPDF2.

---

**httpx / proxies error**
```
TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
```
Run `pip install --upgrade groq "httpx>=0.28.0"` to fix the version conflict.

---

**Scanned PDF — no text extracted**
```
⚠️ Extracted text is empty
```
PyPDF2 cannot read image-based (scanned) PDFs. The PDF must contain selectable text.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## Roadmap

- [ ] OCR support for scanned PDFs
- [ ] Multi-language summarization
- [ ] Batch processing of multiple PDFs
- [ ] Google Drive / Dropbox integration
- [ ] Support for DOCX and TXT files
- [ ] API endpoint for programmatic access

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [Groq](https://groq.com) — ultra-fast LLM inference
- [Streamlit](https://streamlit.io) — web app framework
- [Meta AI](https://ai.meta.com) — Llama models
- [OpenAI](https://openai.com) — GPT-OSS models

---

<div align="center">
Made with Python and Groq
</div>