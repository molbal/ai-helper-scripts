import sys
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import ollama
import re


def clean_text(text):
    """ Clean and format text. """
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
    return text.strip()


def fetch_substack_article(url):
    """ Fetch and extract text content from a Substack article URL. """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract article content
        content = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        article_text = ' '.join([clean_text(tag.get_text()) for tag in content])
        return article_text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""


def main():
    if len(sys.argv) < 2:
        print("Usage: python llm/article.py <Substack Article URLs>")
        sys.exit(1)

    context_articles = []
    for url in sys.argv[1:]:
        article_text = fetch_substack_article(url)
        if article_text:
            context_articles.append(article_text)

    if not context_articles:
        print("No valid articles found. Exiting.")
        sys.exit(1)

    context = ' '.join(context_articles)

    print("Context articles loaded. Please enter your prompt:")
    try:
        prompt = input()
        # Generate LLM prompt
        llm_prompt = f"Based on the style and content of the following context articles:\n{context}\n\nWrite an article on the following topic:\n{prompt}"

        print("")
        print("---- Generated LLM Prompt: ----")
        print("")
        print(llm_prompt)

        stream = ollama.chat(
            model='mistral-nemo',
            messages=[{'role': 'user', 'content': llm_prompt}],
            options={'temperature': 0.5},
            stream=True
        )
        content = ""
        for chunk in stream:
            content += chunk['message']['content']
            print(chunk['message']['content'], end='', flush=True)

        print("")
        print("---- Response ----")
        print("")
        print(content)

    except EOFError:
        print("Exiting.")


if __name__ == "__main__":
    main()
