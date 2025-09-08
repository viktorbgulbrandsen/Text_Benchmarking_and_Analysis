"""
Preprocess Norsk Ordbank into pickled files for faster loading.
Run this once; it will create wordbank.pkl and lemma_data.pkl
in the same directory as this script.
"""

import os
import pickle
from parse_norskordbank import load_wordbank, load_lemma_forms

def main():
    current_dir = os.path.dirname(__file__)

    print("Building wordbank...")
    wordbank = load_wordbank()
    wordbank_path = os.path.join(current_dir, "wordbank.pkl")
    with open(wordbank_path, "wb") as f:
        pickle.dump(wordbank, f)
    print(f"Saved wordbank.pkl ({len(wordbank)} entries)")

    print("Building lemma_forms and form_to_lemma...")
    lemma_forms, form_to_lemma = load_lemma_forms()
    lemma_data_path = os.path.join(current_dir, "lemma_data.pkl")
    with open(lemma_data_path, "wb") as f:
        pickle.dump((lemma_forms, form_to_lemma), f)
    print(f"Saved lemma_data.pkl ({len(lemma_forms)} lemmas, {len(form_to_lemma)} forms)")

if __name__ == "__main__":
    main()