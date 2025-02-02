import sys
import requests
from bs4 import BeautifulSoup
import tqdm
import ollama
import re
from datetime import datetime

from numpy.core.defchararray import upper


def clean_text(text):
    """ Clean and format text. """
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
    return text.strip()

def format_title(text_tag):
    """ Convert title tag to upper case. """
    # Safe check for title tag
    if text_tag:
        return text_tag.get_text().upper()
    return ""

def fetch_substack_article(url):
    """ Fetch and extract text content from a Substack article URL. """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract article content
        content = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        article_text = ' '.join([clean_text(tag.get_text()) for tag in content])
        article_title = soup.find('title')
        return format_title(article_title) + "\n" + article_text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""



def main():
    if len(sys.argv) < 2:
        print("Usage: python llm/article.py <Substack Article URLs>")
        sys.exit(1)

    context_articles = []
    # Fetch URLs with tqdm progress bar
    for url in tqdm.tqdm(sys.argv[1:], desc="Fetching articles"):
        article_text = fetch_substack_article(url)
        if article_text:
            context_articles.append(article_text)

    if not context_articles:
        print("No valid articles found. Exiting.")
        sys.exit(1)

    context = ' '.join(context_articles)
    print("\nContext articles loaded. Please enter context of the new article:")
    try:
        prompt = input()
        # Generate LLM prompt
        llm_prompt = (f"SYSTEM: You are an AI enthusiastic software architect, who believes in consumer rights, privacy and democratization. Dislikes corporate overreach and authoritarian style controls."
                      f"TASK: Please write a an article in the style of the context articles.\n\n"
                      f"NEW ARTICLE CONTEXT:\n{prompt}\n\n"
                      f"RELEVANT ARTICLES:\n{context}")

        # Create timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prompt_filename = f"prompt_{timestamp}.md"
        response_filename = f"response_{timestamp}.md"

        # Save prompt to file
        with open(prompt_filename, 'w') as f:
            f.write(llm_prompt)
        print(f"\nPrompt saved to {prompt_filename}")

        # Generate response
        stream = ollama.chat(
            model='qwen2.5',
            messages=[{'role': 'user', 'content': llm_prompt}],
            options={'temperature': 0.5},
            stream=True
        )

        content = ""
        for chunk in stream:
            content += chunk['message']['content']
            print(chunk['message']['content'], end='', flush=True)

        # Save response to file
        with open(response_filename, 'w') as f:
            f.write(content)
        print(f"\nResponse saved to {response_filename}")

    except EOFError:
        print("\nExiting.")


if __name__ == "__main__":
    main()