
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
3. Run the laravel app
```bash
    php artisan serve
```

## API Reference (Laravel)
> Import curl code in postman to send requests
1. POST /api/get_top_questions
```bash
curl --request GET \
  --url http://localhost:8000/api/get_worst_or_unanswered_questions \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/2023.5.8' \
  --data '{
	"host_url" : "ivfindia.com",
	"num_days": 30
}'
```
2. POST /api/get_worst_or_unanswered_questions
```bash
curl --request GET \
  --url http://localhost:8000/api/get_top_questions \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/2023.5.8' \
  --data '{
	"host_url" : "ivfindia.com",
	"num_days": 30
}'
```


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
