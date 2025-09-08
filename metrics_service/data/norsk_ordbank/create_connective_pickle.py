#!/usr/bin/env python3
# norwegian connectives data

import pickle
import os

def create_connective_data():
    
    connectives = {
        "causal": {
            "fordi", "siden", "da", "derfor", "så", "slik", "dermed", 
            "følgelig", "altså", "på grunn av", "som følge av",
            "ettersom", "idet", "når", "som resultat", "derved"
        },
        
        "coordinating": {
            "og", "eller", "men", "at", "samt", "plus", "minus",
            "enten", "både", "verken", "hverken", "eller"
        },
        
        "subordinating": {
            "at", "hvis", "når", "mens", "til", "før", "etter", 
            "siden", "inntil", "så lenge", "selv om", "enda", 
            "skjønt", "uten at", "med mindre", "dersom", "for å",
            "som om", "som", "hvor"
        },
        
        "temporal": {
            "når", "mens", "før", "etter", "siden", "inntil", "til", 
            "så lenge", "samtidig som", "etter at", "før", "da"
        },
        
        "conditional": {
            "hvis", "dersom", "med mindre", "bare", "så fremt", 
            "forutsatt at", "gitt at"
        },
        
        "all_connectives": set()
    }
    
    for connective_type in ["causal", "coordinating", "subordinating", "temporal", "conditional"]:
        connectives["all_connectives"].update(connectives[connective_type])
    
    return connectives

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "connectives.pkl")
    
    connective_data = create_connective_data()
    
    with open(output_path, "wb") as f:
        pickle.dump(connective_data, f)
    
    print(f"Saved connectives.pkl to {output_path}")

if __name__ == "__main__":
    main()