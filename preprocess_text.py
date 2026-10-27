import glob
import re

HEADING_PATTERNS = [
    # keyword + number/roman numeral alone on a line: "Chapter 12", "Chapter XII.", "PART IV"
    re.compile(
        r"^[ \t]*(?:chapter|part|book|volume|section)[ \t]+(?:\d+|[ivxlcdm]+)[.:]?[ \t]*$",
        re.MULTILINE | re.IGNORECASE,
    ),
    # all-caps headings that also carry a title: "CHAPTER I. Down the Rabbit-Hole"
    re.compile(r"^[ \t]*(?:CHAPTER|PART|BOOK|VOLUME)[ \t]+(?:\d+|[IVXLCDM]]+)\b.*$", re.MULTILINE),
    # lines that are only an uppercase roman numeral: "XII."
    re.compile(r"^[ \t]*[IVXLCDM]+\.?[ \t]*$", re.MULTILINE),
]

HEADING_RE = re.compile(r"^(?i:chapter|part|book|volume|section)\s+(?:\d+|[IVXLCDM]+)\b")
ROMAN_ONLY_RE = re.compile(r"^[IVXLCDM]+\.?$")


def clean_text(text):
    kept = []
    for line in text.splitlines():
        stripped = line.strip()
        if HEADING_RE.match(stripped) or ROMAN_ONLY_RE.match(stripped):
            continue
        kept.append(line)
    return "\n".join(kept)


def load_all_texts(data_folder="data"):
    filepaths = glob.glob(f"{data_folder}/*.txt")
    all_texts = {}

    for filepath in filepaths:
        with open(filepath, "r", encoding="utf-8") as f:
            all_texts[filepath] = f.read()

    return all_texts


def tokenize(text):
    text = clean_text(text)
    text = text.replace("_", "")
    text = text.replace("\u2019", "'")
    text = re.sub(r"\b\d+\b", "", text)
    return re.findall(r"\w+(?:'\w+)?|[.,]", text.lower())


def tokenize_all(all_texts):
    return {filepath: tokenize(text) for filepath, text in all_texts.items()}