import argparse
import json

import streamlit as st
import matplotlib.pyplot as plt
import openai
from bs4 import BeautifulSoup

# Load API key from 'api_key.json'
with open('api_key.json', 'r') as f:
  API_key = json.load(f)['api_key']


def main(args):
    print("APP: Hello form streamlit app")

    st.write("# GPT AI Assistant")
    st.write("Just input link to the article and I will summarize it for you.")

    # example link = https://www.idnes.cz/brno/zpravy/palava-pavlovske-vrchy-zricenina-devicky-oprava.A240516_131402_brno-zpravy_mos1
    link = st.text_input("Link to the article")
    if st.button("Summarize"):
        st.write("Summarizing...")

    if not link:
        return
    
    st.write("Link provided: ", link)
    text = parse_link(link)
    st.write(f"Article title: {text[0]}")

    summarization = summarize(text[1])
    st.write(f"Summary:\n{summarization}")

    question = st.text_input("Ask me a question about the article")
    if not question:
        return
    
    answer = answer_question(text[1], question)
    st.write(f"Answer: {answer}")


def parse_link(link):
    """Parse the link to get the article text using beautifulsoup"""

    return ["Article title", "Article text"]


def summarize(text):
    """Summarize the text using GPT-3 API"""
    oai_client = openai.Client(api_key=API_key)

    article = """Čtvrtý zápas, třetí vítězství. A pořádně cenné. Čeští hokejisté 
    zdolali na domácím mistrovství světa Dánsko 7:4, soupeř ještě ve třetí třetině 
    držel vyrovnaný stav, národní tým ale díky slepeným brankám nakonec uzmul 
    všechny tři body. Konečně se prosadila druhá formace, gólové trápení ukončil Dominik Kubalík."""

    question = "Kdo vyhrál zápas Česko - Dánsko na mistrovství světa v hokeji 2024 a jaké bylo finální skóre?"

    response = oai_client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": article},
            {"role": "user", "content": question}
        ],
    )

    return response.choices[0].message.content


def answer_question(text, question):
    """Answer a question about the text using GPT-3 API"""
    oai_client = openai.Client(api_key=API_key)

    response = oai_client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": text},
            {"role": "user", "content": question}
        ],
    )

    return response.choices[0].message.content


if __name__ == '__main__':
    main()