
# Flask app

## Installation
1.Install requirements
```bash
pip install -r requirements.txt
```

2.Install the Spacy model (en_core_web_md)
```bash
pip install models/en_core_web_md-3.7.0-py3-none-any.whl
```


## Usage
1.Copy the .env.example file to .env and set the OPEN_AI_KEY variable to your OpenAI API key.
```bash
    cp .env.example .env
```
2.Run the app
```bash
    python app.py
```

## API Reference (Laravel)
1. POST /api/get_top_questions
    - JSON: {
        "host_url": string | required,
        "num_days": int | optional (default: 10),
    }

2. POST /api/get_worst_or_unanswered_questions
    - JSON: {
        "host_url": string | required,
        "num_days": int | optional (default: 10),
    }


## File structure
- helpers
    - aggregate.py
    - formatters.py
    - optimizer.py 

- models 
    - en_core_web_sm-3.7.0-py3-none-any.whl
    - en_core_web_md-3.7.0-py3-none-any.whl
- app.py: Flask app
- .gitignore: Files to ignore
- requirements.txt: Python dependencies
- .env.example: Example .env file
- README.md: This file
