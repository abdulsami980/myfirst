import streamlit as st
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

st.set_page_config(page_title="Article GPT")

st.sidebar.title("Article Summarizer")

# Text input for the article URL
article_url = st.sidebar.text_input("Enter the URL of the article:")

# Max length input
max_length = st.sidebar.number_input("Max Length for Summary", min_value=1, max_value=300, value=90)

# Min length input
min_length = st.sidebar.number_input("Min Length for Summary", min_value=1, max_value=300, value=30)

# Button to summarize the article
if st.sidebar.button("Summarize"):
    if article_url:
        # Function to fetch and summarize an article from a URL
        def summarize_article_from_url(url, max_length, min_length):
            try:
                response = requests.get(url)
                if response.status_code != 200:
                    return "Failed to fetch the article content."

                soup = BeautifulSoup(response.text, "html.parser")

                article_text = " ".join([p.get_text() for p in soup.find_all('p')])

                chunks = [article_text[i:i+1024] for i in range(0, len(article_text), 1024)]

                summaries = []

                for chunk in chunks:
                    summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
                    summaries.append(summary[0]['summary_text'])

                overall_summary = " ".join(summaries)

                return overall_summary
            except Exception as e:
                return str(e)

        # Summarize the article and display the result
        with st.spinner("Summarizing..."):
            summary = summarize_article_from_url(article_url, max_length, min_length)
            st.subheader("Summary:")
            st.write(summary)
    else:
        st.warning("Please enter a valid article URL.")
