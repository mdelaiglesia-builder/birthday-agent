import argparse
import string
from collections import Counter

parser = argparse.ArgumentParser(description="Count words in a file")
parser.add_argument("filepath", help="Path to the file to analyze")
args = parser.parse_args()

try:
    with open(args.filepath) as f:
        content = f.read()
        extra_punctuation = "—–''""…"
        cleaned = content.lower().translate(str.maketrans('', '', string.punctuation + extra_punctuation))
        lines = cleaned.lower().splitlines()
        print(len(lines))
        words = cleaned.lower().split()
        print(len(words))
        five_most_common = Counter(words).most_common(5)
        for w in five_most_common:
            print(w)
except FileNotFoundError:
    print(f"Error: file '{args.filepath}' not found.")