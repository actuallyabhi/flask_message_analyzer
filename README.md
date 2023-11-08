
# Flask app

## Installation

```bash
pip install -r requirements.txt
```

## Usage
1.Copy the .env.example file to .env and set the OPEN_AI_KEY variable to your OpenAI API key.

2.Run the app
```bash
    python app.py
```

## API Reference (laravel)
1. POST /api/get_top_questions
    - JSON: {
        "host_url": string | required,
        "num_days": int | optional,
    }

2. POST /api/get_worst_or_unanswered_questions
    - JSON: {
        "host_url": string | required,
        "num_days": int | optional,
    }

# File structure
- en_core_web_sm: Spacy model
- helpers
    -aggregate.py
    -formatters.py
    -optimizer.py 
- app.py: Flask app
- .gitignore: Files to ignore
- requirements.txt: Python dependencies
- .env.example: Example .env file
- README.md: This file
