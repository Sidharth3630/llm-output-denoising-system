# LLM Output Denoising System

A beginner-friendly multi-agent app that improves raw LLM answers using CrewAI agents and Groq (Llama 3).

## What it does
1. User enters a question in the Streamlit UI
2. System generates a **raw** response via Groq
3. A **5-step multi-agent workflow** refines the response:
   - Fact Checking
   - Consistency Validation
   - Conciseness
   - Style & Grammar
   - Final Review
4. The UI shows the output (and basic before/after metrics).

> Note: This repo’s agent implementations focus on modular structure and beginner-friendly readability.

## Project structure
```
project/
│
├── agents/
│   ├── fact_checker.py
│   ├── consistency_agent.py
│   ├── concise_agent.py
│   ├── style_agent.py
│   └── final_review.py
│
├── app.py
├── requirements.txt
├── .env
├── crew_setup.py
├── utils.py
└── README.md
```

## Setup (Windows)

### 1) Create virtual environment
From this project folder:
```bat
python -m venv .venv
.venv\Scripts\activate
```

### 2) Install dependencies
```bat
pip install -r requirements.txt
```

### 3) Add your Groq API key
Create a file named `.env` in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=
```

### 4) Run Streamlit
```bat
streamlit run app.py
```

Then open the URL shown in the terminal.

## Troubleshooting
- If you see `GROQ_API_KEY not found...`, confirm your `.env` file is in the project root.
- If CrewAI fails at runtime, ensure `crewai` is installed per `requirements.txt`.

# llm-output-denoising-system
