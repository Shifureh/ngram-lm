import glob
import re


def load_all_texts(data_folder="data"):
    # Load each text file in the data folder into a dict, keyed by filepath
    filepaths = glob.glob(f"{data_folder}/*.txt")
    all_texts = {}

    for filepath in filepaths:
        with open(filepath, "r", encoding="utf-8") as f:
            all_texts[filepath] = f.read()

    return all_texts


def tokenize(text):
    # Lowercase and split text by words and punctuation.
    text = text.replace("_", "")
    text = re.sub(r"\b\d+\b", "", text)  # remove standalone numbers (line markers)
    return re.findall(r"\w+(?:'\w+)?|[.,]", text.lower())


def tokenize_all(all_texts):
    # Apply tokenize() to every text in the dict, keeping the same keys.
    return {filepath: tokenize(text) for filepath, text in all_texts.items()}


if __name__ == "__main__":
    raw_texts = load_all_texts()
    tokenized_texts = tokenize_all(raw_texts)
    for filepath, tokens in tokenized_texts.items():
        print(filepath)
        print(tokens)
        print("---\n")
