import os
import argparse
from tqdm import tqdm
import ollama


def load_few_shot_examples(file_path):
    """
    Load few-shot examples from a file.
    """
    with open(file_path, 'r') as file:
        return file.read()


def rewrite_description(description, few_shot_examples, model_name):
    """
    Use the local LLM to rewrite the description into tag-based format.
    """
    prompt = (
        f"{few_shot_examples}\n"
        f"Rewrite the following description into a tag-based format. Use commas to separate tags. Remove mediums such as painting, cartoon:\n"
        f"Input: {description}\n"
        f"Output:"
    )

    response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content'].strip()


def main():
    parser = argparse.ArgumentParser(description="Rewrite descriptions in text files to tag-based format.")
    parser.add_argument("directory", type=str, help="Directory containing text files to process.")
    parser.add_argument("--model_name", type=str, help="Name of the LLM model to use.", default="llama3")
    parser.add_argument("--examples_file", type=str, help="File containing few-shot examples.", default="prompts/description-to-tags-examples.txt")
    args = parser.parse_args()

    few_shot_examples = load_few_shot_examples(args.examples_file)

    for filename in tqdm(os.listdir(args.directory), desc="Rewriting descriptions", unit="caption"):
        if filename.endswith('.txt'):
            file_path = os.path.join(args.directory, filename)

            # Read the content of the file
            with open(file_path, 'r') as file:
                original_content = file.read()

            # Rewrite the content using the local LLM
            new_content = rewrite_description(original_content, few_shot_examples, args.model_name)

            # Print the 'from' and 'to' values
            print(f"\nFile: {file_path}")
            print(f"\nFrom: {original_content}")
            print(f"To: {new_content}\n")

            # Clear the original content and save the new content
            with open(file_path, 'w') as file:
                file.write(new_content)


if __name__ == "__main__":
    main()
