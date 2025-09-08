# norsk ordbank parser

import tarfile
import os
from typing import Set
from typing import Dict, Set, Tuple


def load_wordbank() -> Set[str]:
    # load norwegian words from ordbank
    current_dir = os.path.dirname(__file__)
    tar_path = os.path.join(current_dir, "20220201_norsk_ordbank_nob_2005.tar.gz")
    
    if not os.path.exists(tar_path):
        raise FileNotFoundError(f"Norsk Ordbank file not found: {tar_path}")
    
    words = set()
    
    with tarfile.open(tar_path, 'r:gz') as tar:
        try:
            member = tar.getmember('fullformsliste.txt')
            file_obj = tar.extractfile(member)
            
            if file_obj is None:
                raise ValueError("Could not extract fullformsliste.txt from archive")
            
            # Read and parse the tab-separated file
            for line_num, line in enumerate(file_obj):
                # Skip header line
                if line_num == 0:
                    continue
                    
                line_str = line.decode('latin1').strip()
                if not line_str:
                    continue
                
                # Split by tab and get the OPPSLAG column (index 2)
                parts = line_str.split('\t')
                if len(parts) >= 3:
                    word = parts[2].strip().lower()
                    # Filter out symbols, numbers, and empty entries
                    if word and word.isalpha() and len(word) > 1:
                        words.add(word)
                        
        except KeyError:
            raise ValueError("fullformsliste.txt not found in the tar.gz archive")
    
    return words

def load_lemma_forms() -> Tuple[Dict[str, Set[str]], Dict[str, str]]:
    # lemma forms and form-to-lemma mapping
    current_dir = os.path.dirname(__file__)
    tar_path = os.path.join(current_dir, "20220201_norsk_ordbank_nob_2005.tar.gz")

    if not os.path.exists(tar_path):
        raise FileNotFoundError(f"Norsk Ordbank file not found: {tar_path}")

    lemma_forms: Dict[str, Set[str]] = {}
    form_to_lemma: Dict[str, str] = {}

    with tarfile.open(tar_path, 'r:gz') as tar:
        try:
            member = tar.getmember("fullformsliste.txt")
            file_obj = tar.extractfile(member)
            if file_obj is None:
                raise ValueError("Could not extract fullformsliste.txt from archive")

            for line_num, line in enumerate(file_obj):
                if line_num == 0:
                    continue  # header
                parts = line.decode("latin1").strip().split("\t")
                if len(parts) >= 3:
                    lemma = parts[1].strip().lower()
                    form = parts[2].strip().lower()
                    if lemma and form and form.isalpha():
                        lemma_forms.setdefault(lemma, set()).add(form)
                        form_to_lemma[form] = lemma

        except KeyError:
            raise ValueError("fullformsliste.txt not found in archive")

    return lemma_forms, form_to_lemma
