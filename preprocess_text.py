import glob

def load_all_texts(data_folder="data"):
    filepaths = glob.glob(f"{data_folder}/*.txt")
    all_texts = {}
    
    for filepath in filepaths:
        # load each text file in the data folder into a dict, keyed by filepath
        with open(filepath, "r", encoding="utf-8") as f:
            all_texts[filepath] = f.read()

    return all_texts

raw_text = load_all_texts()

for filepath, text in raw_text.items():
    print(filepath)
    print(text)
    print("---\n")