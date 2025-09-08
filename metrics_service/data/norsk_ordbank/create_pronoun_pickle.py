

import pickle
import os

def create_pronoun_data():
    # norwegian pronoun data
    
    pronouns = {
        "first_person": {
            "jeg", "meg", "min", "mitt", "mine",
            "vi", "oss", "vår", "vårt", "våre"
        },
        
        "second_person": {
            "du", "deg", "din", "ditt", "dine",
            "dere", "deres"
        },
        
        "third_person": {
            "han", "ham", "hans",
            "hun", "henne", "hennes", 
            "det", "den",
            "sin", "sitt", "sine", "seg",
            "de", "dem", "deres"
        },
        
        "all_pronouns": set()
    }
    
    for person_pronouns in [pronouns["first_person"], pronouns["second_person"], pronouns["third_person"]]:
        pronouns["all_pronouns"].update(person_pronouns)
    
    return pronouns

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "pronouns.pkl")
    
    pronoun_data = create_pronoun_data()
    
    
    with open(output_path, "wb") as f:
        pickle.dump(pronoun_data, f)
    
    print(f"Saved pronouns.pkl to {output_path}")

if __name__ == "__main__":
    main()