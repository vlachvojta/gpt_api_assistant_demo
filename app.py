import argparse
import json
import requests
from urllib.request import urlopen

import streamlit as st
import matplotlib.pyplot as plt
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
    if st.button("Summarize"):
        st.write("Summarizing...")

    if not link:
        return

    text = parse_link(link)
    st.write(f"## {text[0]}")

    summarization = summarize(text[1])
    st.write(f"Summary:\n{summarization}")

    question = st.text_input("Ask me a question about the article")
    if not question:
        return
    
    answer = answer_question(text[1], question)
    st.write(f"Answer: {answer}")


def parse_link(link):
    """Parse the link to get the article text using beautifulsoup"""
    # download html from link
    response = requests.get(link)
    html_content = response.text

    # Step 3: Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')  # You can also use 'html.parser'
    # print(soup.prettify()[:500])
    # return '', ''

    # page = urlopen(link)

    # try:
    #     html = page.read().decode("ISO-8859-1")
    # except UnicodeDecodeError:
    #     html = page.read().decode("utf-8")

    # soup = BeautifulSoup(html, "html.parser")

    # # export soup to html file
    # with open("soup.html", "w") as file:
    #     file.write(str(soup))

    # print(f'Soup saved to soup.html')
    # print(str(soup)[:500])

    # parse html using beautifulsoup
    article_title = soup.find('h1').text
    article_text = ''  # soup.find('div', {'class': 'article-text'}).text

    if soup.find('div', {'class': 'bbtext'}) is None:
        raise ValueError("The article text is not in the expected format.")

    for p in soup.find('div', {'class': 'bbtext'}).findAll('p'):
        article_text += p.text + '\n'

    return article_title, article_text


def summarize(text):
    """Summarize the text using GPT-3 API"""
    oai_client = openai.Client(api_key=API_key)

    # article = """Čtvrtý zápas, třetí vítězství. A pořádně cenné. Čeští hokejisté 
    # zdolali na domácím mistrovství světa Dánsko 7:4, soupeř ještě ve třetí třetině 
    # držel vyrovnaný stav, národní tým ale díky slepeným brankám nakonec uzmul 
    # všechny tři body. Konečně se prosadila druhá formace, gólové trápení ukončil Dominik Kubalík."""

    # question = "Kdo vyhrál zápas Česko - Dánsko na mistrovství světa v hokeji 2024 a jaké bylo finální skóre?"

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