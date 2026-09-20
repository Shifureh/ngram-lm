import glob
import re


def load_all_texts(data_folder="data"):
    filepaths = glob.glob(f"{data_folder}/*.txt")
    all_texts = {}

    for filepath in filepaths:
        with open(filepath, "r", encoding="utf-8") as f:
            all_texts[filepath] = f.read()

    return all_texts


def tokenize(text):
    text = text.replace("_", "")
    text = text.replace("\u2019", "'")
    text = re.sub(r"\b\d+\b", "", text)
    return re.findall(r"\w+(?:'\w+)?|[.,]", text.lower())


def tokenize_all(all_texts):
    return {filepath: tokenize(text) for filepath, text in all_texts.items()}