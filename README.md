# Restaurant Name Generator using LangChain

An AI-powered web application that generates creative restaurant names and suggested menu items based on selected cuisine using LangChain and OpenAI.


## Overview

This project leverages Large Language Models (LLMs) to assist entrepreneurs, developers, and creatives in generating:

- Unique restaurant names
- Relevant menu suggestions
- Cuisine-based branding ideas

Built with:
- LangChain
- OpenAI API
- Streamlit (UI)


## Features

- Generate restaurant names based on cuisine
- Suggest menu items automatically
- Fast and interactive UI with Streamlit
- Uses LLMs for intelligent text generation


## Tech Stack

| Technology | Purpose |
|-----------|--------|
| Python | Core Programming |
| LangChain | LLM Orchestration |
| OpenAI API | Text Generation |
| Streamlit | Web Interface |

## Project Structure

```
.
├── RestaurantNameGenerator/
│   ├── main.py              # Streamlit App
│   ├── langchain_helper.py # LLM logic
│   └── secret_key.py       # API keys (not for production)
│
├── langchain_crashcourse.ipynb  # Learning notebook
├── requirements.txt             # Dependencies
└── README.md
```


## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/restaurant-name-generator.git
cd restaurant-name-generator
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup API Keys

Update your API keys inside:

```python
# secret_key.py
openapi_key = "YOUR_OPENAI_API_KEY"
serpapi_key = "YOUR_SERPAPI_KEY"
```

Important:
Do not upload API keys to GitHub. Use environment variables in production.


## Run the Application

```bash
streamlit run RestaurantNameGenerator/main.py
```


## Deployment

You can deploy this app using:

- Streamlit Cloud
- Railway
- Render


## Demo

Add screenshots or demo link here.


## Learning Resource

This project is inspired by a LangChain tutorial and includes a notebook for learning:

- langchain_crashcourse.ipynb


## Future Improvements

- Add logo generation
- Multi-language support
- Save generated results
- User authentication



