import argparse
import json
import requests
from urllib.request import urlopen

import streamlit as st
import openai
from bs4 import BeautifulSoup


# Load API key from 'api_key.json'
with open('api_key.json', 'r') as f:
  API_key = json.load(f)['api_key']


def main():
    print("APP: Hello form streamlit app")

    st.write("# GPT AI Assistant")
    st.write("Just input link to the article and I will summarize it for you.")

    # example link = https://www.idnes.cz/brno/zpravy/palava-pavlovske-vrchy-zricenina-devicky-oprava.A240516_131402_brno-zpravy_mos1
    link = st.text_input("Link to the article")

    if not link:
        return

    text = parse_link(link)
    st.write(f"## {text[0]}")

    summarization = summarize(text[1])
    st.write(f"**Summary**: {summarization}")

    question = st.text_input("Ask me a question about the article")
    if not question:
        return
    
    answer = answer_question(text[1], question)
    st.write(f"**Answer**: {answer}")


def parse_link(link):
    """Parse the link to get the article text using beautifulsoup"""
    # download html from link
    response = requests.get(link)
    html_content = response.text

    # parse html using beautifulsoup
    soup = BeautifulSoup(html_content, 'html.parser')
    article_title = soup.find('h1').text
    article_text = ''

    if soup.find('div', {'class': 'bbtext'}) is None:
        return article_title, article_text

    # get all paragraphs from the article (inside div with class 'bbtext')
    for p in soup.find('div', {'class': 'bbtext'}).findAll('p'):
        article_text += p.text + '\n'

    return article_title, article_text


def summarize(text):
    """Summarize the text using GPT-3 API"""
    oai_client = openai.Client(api_key=API_key)

    response = oai_client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are friendly and helpful chatbot and you provide a short summarization of a given text in czech."},
            {"role": "user", "content": "The text is:\n" + text}
        ],
    )

    return response.choices[0].message.content


def answer_question(text, question):
    """Answer a question about the text using GPT-3 API"""
    oai_client = openai.Client(api_key=API_key)

    response = oai_client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are friendly and helpful chatbot and you answer a question based on given text in czech."},
            {"role": "system", "content": "The text is:\n" + text},
            {"role": "user", "content": "The question is:\n" + question}
        ],
    )

    return response.choices[0].message.content


if __name__ == '__main__':
    main()