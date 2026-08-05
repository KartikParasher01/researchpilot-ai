# 🔍 ResearchPilot AI

An AI-powered research assistant that searches the web, extracts relevant articles, analyzes multiple sources using an LLM, and generates structured research reports through a clean Gradio interface.

> Search → Scrape → Analyze → Summarize → Report


## ✨ Features

- 🔎 Search the web using Tavily Search API
- 🌐 Scrape article content using BeautifulSoup
- 🧹 Clean and preprocess webpage text
- 🤖 Generate structured research reports using Groq LLM
- 📑 Return:
  - Summary
  - Key Points
  - Detailed Analysis
  - Confidence Score
  - Sources
- 🖥️ Interactive Gradio UI
- ✅ Structured JSON validation using Pydantic

  ## Architecture
                         +------------------+
                         |     User         |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |    Gradio UI     |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |  research.py     |
                         +--------+---------+
                                  |
              +-------------------+-------------------+
              |                   |                   |
              v                   v                   v
      +---------------+   +---------------+   +---------------+
      |  search.py    |   |  scraper.py   |   |    llm.py     |
      +---------------+   +---------------+   +---------------+
              |                   |                   |
              +-------------------+-------------------+
                                  |
                                  v
                         +------------------+
                         | Research Report  |
                         +------------------+


## Tech Stack

Python
Gradio
Groq


## Folder Structure

ResearchPilot_AI/

├── app.py
├── src/
│   ├── search.py
│   ├── scraper.py
│   ├── llm.py
│   ├── prompts.py
│   ├── models.py
│   ├── config.py
│   └── research.py
│
├── requirements.txt
└── README.md



## Learning Outcomes
### What I Learned

- API Integration
- Web Scraping
- Prompt Engineering
- LLM Applications
- Pydantic Validation
- Gradio
- Python Generators (coming soon)

## Future Improvements

- Streaming responses
- PDF report export
- Dark/Light theme
- Citation scoring
- Multi-model support
- RAG integration
- Search history


## Result Preview

![ResearchPilot AI result preview](Screenshot.png)

