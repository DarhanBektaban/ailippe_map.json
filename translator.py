import json
import re
import os

class AilippeTranslator:
    def __init__(self, map_file="ailippe_map.json"):
        self.map_data = self._load_map(map_file)
        self._build_forward_maps()
        self._build_reverse_maps()

    def _load_map(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Mapping file '{filepath}' not found.")
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _build_forward_maps(self):
        """Prepares dictionaries for Cyrillic -> Latin conversion."""
        logic = self.map_data['logic']['forward']
        
        # 1. Special Rules (Prioritized replacements)
        self.fwd_special = sorted(
            logic.get('special_rules', []), 
            key=lambda x: x['priority'], 
            reverse=True
        )
        
        # 2. Char Maps (Merge Core and Loan)
        self.fwd_chars = {**logic['core_map'], **logic['loan_map']}
        # Remove meta keys like 'description' if they exist in the maps
        self.fwd_chars.pop('description', None)

    def _build_reverse_maps(self):
        """Prepares dictionaries for Latin -> Cyrillic conversion."""
        logic = self.map_data['logic']['reverse']
        
        # Merge token_map and single_char_map
        combined_map = {**logic['token_map'], **logic['single_char_map']}
        combined_map.pop('description', None) # Clean up
        
        # SORTING IS CRITICAL: Longest tokens must be matched first (e.g., 'shch' before 'sh')
        self.rev_tokens = sorted(combined_map.keys(), key=len, reverse=True)
        self.rev_map = combined_map

    def _match_case(self, original, transformed):
        """
        Helper to restore casing of the transformed text based on the original.
        Handles: "Word"->"Word", "WORD"->"WORD", "word"->"word".
        """
        if original.isupper():
            return transformed.upper()
        if original.istitle():
            return transformed.title()
        return transformed.lower()

    def cyrillic_to_latin(self, text):
        """
        Converts Cyrillic text to Darhan Bektaban Latin.
        """
        if not text: return ""

        # 1. Apply Special Rules first (e.g., ция -> sja)
        # We perform a case-insensitive search but case-aware replacement
        for rule in self.fwd_special:
            src = rule['input']
            tgt = rule['output']
            
            # Regex to find the pattern (case insensitive)
            pattern = re.compile(re.escape(src), re.IGNORECASE)
            
            # Callback function to replace while preserving case
            def replace_callback(match):
                return self._match_case(match.group(), tgt)
            
            text = pattern.sub(replace_callback, text)

        # 2. Apply Character Mapping
        result = []
        for char in text:
            lower_char = char.lower()
            if lower_char in self.fwd_chars:
                mapped = self.fwd_chars[lower_char]
                result.append(self._match_case(char, mapped))
            else:
                result.append(char) # Keep unknown chars (punctuation, numbers)
        
        return "".join(result)

    def latin_to_cyrillic(self, text):
        """
        Converts Darhan Bektaban Latin to Cyrillic using Greedy Tokenization.
        Note: Ambiguities (j -> й/и) use the default map defined in JSON.
        """
        if not text: return ""
        
        result = []
        i = 0
        n = len(text)

        while i < n:
            match_found = False
            
            # Try to match the longest possible token starting at i
            for token in self.rev_tokens:
                token_len = len(token)
                
                # Check bounds and equality (case insensitive comparison)
                if (i + token_len <= n) and (text[i:i+token_len].lower() == token):
                    original_segment = text[i:i+token_len]
                    cyrillic_segment = self.rev_map[token]
                    
                    # Apply Case Logic
                    result.append(self._match_case(original_segment, cyrillic_segment))
                    
                    i += token_len
                    match_found = True
                    break
            
            if not match_found:
                # If no token matches, keep the character as is
                result.append(text[i])
                i += 1
                
        return "".join(result)

# --- Usage Example ---
if __name__ == "__main__":
    try:
        translator = AilippeTranslator()
        
        print(f"--- {translator.map_data['meta']['project_name_primary']} v{translator.map_data['meta']['version']} ---")
        print(f"Loaded by: {translator.map_data['meta']['author']}\n")

        # Test Data
        test_words = [
            "Қазақстан", 
            "Энциклопедия", 
            "Авиация",   # Tests special rule 'ция' -> 'sja'
            "Юбилей",    # Tests 'ю' -> 'juu'
            "Шымкент",   # Tests 'ш' -> 'sh'
            "Вагон"      # Tests loan 'в' -> 'v'
        ]

        print(f"{'Cyrillic Input':<20} | {'Latin Output':<20} | {'Reverse Check':<20}")
        print("-" * 66)

        for word in test_words:
            latin = translator.cyrillic_to_latin(word)
            reverse = translator.latin_to_cyrillic(latin)
            print(f"{word:<20} | {latin:<20} | {reverse:<20}")

        print("\n--- Collision / Ambiguity Note ---")
        print("Note: Reverse mapping uses default rules. E.g., 'j' maps to 'й' by default, though it could be 'и'.")
        print(f"Test 'j': {translator.latin_to_cyrillic('j')} (Context agnostic)")

    except Exception as e:
        print(f"Error: {e}")
