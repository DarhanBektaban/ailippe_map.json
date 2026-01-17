import json
import os

def load_mapping(filename="ailippe_map.json"):
    # Looks for the json file in the same folder as this script
    if not os.path.exists(filename):
        return None
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def to_ailippe(text, data):
    if not data:
        return "Error: Mapping file not found."
        
    # 1. Load Logic
    logic = data["logic"]["forward"]
    result = text.lower()
    
    # 2. Apply Special Rules (Priority) first
    for rule in logic["special_rules"]:
        result = result.replace(rule["input"], rule["output"])
        
    # 3. Apply Standard Map
    mapping = logic["standard_map"]
    new_text = ""
    for char in result:
        # If the char is in our map, swap it. If not, keep it (like punctuation).
        new_text += mapping.get(char, char) 
        
    # Capitalize the first letter of the sentence
    return new_text.capitalize()

# --- Test Run ---
if __name__ == "__main__":
    data = load_mapping()
    
    # Simple Test
    test_word = "Қазақстан"
    if data:
        print(f"Original: {test_word}")
        print(f"Result:   {to_ailippe(test_word, data)}")
    else:
        print("Could not find ailippe_map.json")
