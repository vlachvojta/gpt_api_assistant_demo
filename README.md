# GPT API assistant demo - Streamlit (python) web app

- [x] input article url (from specific news site: [idnes.cz](https://www.idnes.cz/))
- [x] scrape text of the article
- [x] summarize article using openai api
- [x] ask a question
- [x] give answer based on the article

## Componnents
- web scraper
- GPT API client
- Streamlit (python) web IO

## Instalation and run
Start by installing dependencies with: <br>
```pip install -r requirements.txt```

Run with: <br>
```streamlit run app.py```

To use the GPT API feature, save your API key to `api_key.json` file in the format of `api_key_template.json`
