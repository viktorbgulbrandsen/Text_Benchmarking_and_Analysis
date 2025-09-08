#!/usr/bin/env python3
# pos categories from fullformsliste.txt

import pickle
import os
from typing import Set, Dict

def extract_pos_categories() -> Dict[str, Set[str]]:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fullforms_path = os.path.join(current_dir, "fullformsliste.txt")
    
    if not os.path.exists(fullforms_path):
        raise FileNotFoundError(f"fullformsliste.txt not found at {fullforms_path}")
    
    pos_categories = {
        "nouns": set(),           
        "adjectives": set(),       
        "verbs": set(),          
        "adverbs": set(),        
        "content_words": set(),  
        "function_words": set()  
    }
    
    
    with open(fullforms_path, 'r', encoding='utf-8', errors='ignore') as f:
        next(f)
        
        line_count = 0
        for line in f:
            line_count += 1
            if line_count % 100000 == 0:
                print(f"Processed {line_count} lines...")
            
            try:
                parts = line.strip().split('\t')
                if len(parts) < 4:
                    continue
                    
                word = parts[2].lower()  # OPPSLAG column (the word form)
                tag = parts[3].lower()   # TAG column (POS tag)
                
                if not word or len(word) < 2:
                    continue
                
                # Categorize based on POS tag
                if 'subst' in tag:  # substantiv (noun)
                    pos_categories["nouns"].add(word)
                    pos_categories["content_words"].add(word)
                elif 'adj' in tag:  # adjektiv (adjective)
                    pos_categories["adjectives"].add(word)
                    pos_categories["content_words"].add(word)
                elif 'verb' in tag:  # verb
                    pos_categories["verbs"].add(word)
                    pos_categories["content_words"].add(word)
                elif 'adv' in tag:  # adverb
                    pos_categories["adverbs"].add(word)
                    pos_categories["content_words"].add(word)
                else:
                    # Function words: pronouns, prepositions, conjunctions, etc.
                    if any(func_tag in tag for func_tag in ['pron', 'prep', 'konj', 'interj', 'det']):
                        pos_categories["function_words"].add(word)
                        
            except Exception as e:
                # Skip problematic lines
                continue
    
    print(f"Finished processing {line_count} lines")
    return pos_categories

def main():
    # save pos categories
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "pos_categories.pkl")
    
    pos_data = extract_pos_categories()
    
    
    with open(output_path, "wb") as f:
        pickle.dump(pos_data, f)
    
    print(f"Saved pos_categories.pkl to {output_path}")

if __name__ == "__main__":
    main()