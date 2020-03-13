import os

base_path = os.path.dirname(__file__)

def load_hangul(hangul):
    # Read the file and returns all words in it.
    with open(os.path.join(base_path, "data", hangul), "r", encoding="utf8", errors="ignore") as f:
        return [c for c in f.read().splitlines() if len(c) > 0]

def load_num(number):
    # Read the file and returns all numbers in it.
    with open(os.path.join(base_path, "data", number), "r", encoding="utf-8", errors="ignore") as f:
        return [n for n in f.read().splitlines() if n.isdigit()]

def load_fonts(font_path):
    # Load all fonts in the fonts directories
    return [os.path.join(base_path, font_path, font)
            for font in os.listdir(os.path.join(base_path, font_path)) if font.lower().endswith('.ttf')]
