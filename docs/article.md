## Article Generation

### Overview

The `article.py` script is designed to generate articles based on the style and content of provided Substack article URLs.
It fetches the text content from the specified URLs, cleans and formats the text, and then uses an LLM to generate an article on the provided topic.

#### High-Level Functionality

1. **Fetch article content**: Retrieves the text content from the specified Substack article URLs.
2. **Clean and format text**: Removes unnecessary characters, replaces multiple whitespace with single space, and strips leading/trailing whitespace.
3. **Generate LLM prompt**: Creates a prompt for the LLM based on the context articles and the user-provided topic.
4. **Generate article**: Uses the LLM to generate an article based on the prompt.

#### Dependencies

Ensure the following dependencies are installed before running the script:

- Python 3.6 or higher
- `requests` for fetching article content
- `BeautifulSoup` for parsing HTML content
- `tqdm` for progress bars
- `ollama` for local language model interaction

Install them using pip:
```sh
pip install requests beautifulsoup4 tqdm ollama
```

#### CLI Parameters

| Parameter                 | Description                                             | Example                                                                             |
|---------------------------|---------------------------------------------------------|-------------------------------------------------------------------------------------|
| `<Substack Article URLs>` | One or more Substack article URLs to fetch content from | `https://example.substack.com/p/article-1 https://example.substack.com/p/article-2` |

#### Usage

To use this script, run it from the command line with the Substack article URLs as arguments:
```sh
python llm/article.py <Substack Article URLs>
```
Replace `<Substack Article URLs>` with the actual URLs of the articles you want to use as context.

#### Notes

- The script will prompt the user to enter a topic for the generated article.
- The script uses the `mistral-nemo` LLM model by default, but this can be changed by modifying the `model` parameter in the `ollama.chat` function.
- The script will print the generated LLM prompt and the response from the LLM.
- If the script encounters any errors while fetching article content, it will print an error message and continue with the next URL.