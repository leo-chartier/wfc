##################################
#                                #
#   Generator for the "python"   #
#        tileset and rules       #
#                                #
##################################

RULE_NAME = "python" # Used for the .json file and the folder

FONT_MAPPING_URL = "https://raw.githubusercontent.com/sunaku/tamzen-font/master/screenshot.txt"
SPRITESHEET_URL = "https://raw.githubusercontent.com/sunaku/tamzen-font/master/png/Tamzen6x12r.png"
SPRITE_SIZE = 6 # Assumes that this is the width and 1/2 the height of a character
EXTRACT_ROWS = range(1, 4) # The first row is the filename. We only care about the next 3.

from settings import *

BACKGROUND = "#1F1F1F"
COLORS = {
    Token.Comment: "#6A9955",
    Token.Variable: "#9CDCFE",
    Token.Constant: "#4FC1FF",
    Token.Numeric: "#B5CEA8",
    Token.Operator: "#D4D4D4",
    Token.Namespace: "#4EC9B0",
    Token.Function: "#DCDCAA",
    Token.Control: "#C586C0",
    Token.Whitespace: BACKGROUND,
}





import json
import os
from PIL import Image
from PIL.ImageOps import invert
import re
import requests
import shutil



CHAR_WIDTH = SPRITE_SIZE
CHAR_HEIGHT = 2 * SPRITE_SIZE

TOP_CROP = (0, 0, SPRITE_SIZE, SPRITE_SIZE)
BOTTOM_CROP = (0, SPRITE_SIZE, SPRITE_SIZE, 2 * SPRITE_SIZE)

ROOT = os.path.dirname(os.path.dirname(__file__))
SPRITE_DIR_PATH = os.path.join(ROOT, RULE_NAME)
RULES_PATH = os.path.join(ROOT, RULE_NAME + ".json")

def get_sprite_name(symbol: Symbol, char: str, bottom: bool) -> str:
    return f"{symbol.name}_{ord(char)}{'_'*bottom}"



# Get the spritesheet
spritesheet = Image.open(requests.get(SPRITESHEET_URL, stream=True).raw)
spritesheet = invert(spritesheet.convert("L")) # Make it white on black
offset_x = (spritesheet.width % CHAR_WIDTH) // 2
offset_y = (spritesheet.height % CHAR_HEIGHT) // 2

# Fetch the character mapping
mapping_lines = requests.get(FONT_MAPPING_URL).text.splitlines()
char_to_coords = {
    char: (j * CHAR_WIDTH + offset_x, i * CHAR_HEIGHT + offset_y)
    for i in EXTRACT_ROWS
    for j, char in enumerate(mapping_lines[i - EXTRACT_ROWS.start])
}

# Extract the sprites
char_to_mask = {
    char: spritesheet.crop((x, y, x + CHAR_WIDTH, y + CHAR_HEIGHT))
    for char, (x, y) in char_to_coords.items()
}

# Extract the possible characters for each symbols
symbol_to_chars: dict[Symbol, list[str]] = {}
for symbol in Symbol.ALL:
    symbol_to_chars[symbol] = []
    for char, mask in char_to_mask.items():
        if re.match(symbol.pattern, char):
            symbol_to_chars[symbol].append(char)



# Remove old sprites if any
if os.path.isdir(SPRITE_DIR_PATH):
    shutil.rmtree(SPRITE_DIR_PATH)
os.mkdir(SPRITE_DIR_PATH)

# Generate the sprites
for symbol in Symbol.ALL:
    for char in symbol_to_chars[symbol]:
        color = Image.new("RGB", mask.size, COLORS[symbol.token])
        sprite = Image.new("RGB", mask.size, BACKGROUND)
        mask = char_to_mask[char]
        sprite.paste(color, mask=mask)

        top_fn = get_sprite_name(symbol, char, False)
        top_fp = os.path.join(SPRITE_DIR_PATH, top_fn + ".png")
        sprite.crop(TOP_CROP).save(top_fp)

        bottom_fn = get_sprite_name(symbol, char, True)
        bottom_fp = os.path.join(SPRITE_DIR_PATH, bottom_fn + ".png")
        sprite.crop(BOTTOM_CROP).save(bottom_fp)



# Prepare the rules
rules: dict[str, dict[str, str | int | set[str] | list[str]]] = {}
all_top_names: set[str] = set()
all_bottom_names: set[str] = set()
for symbol in sorted(symbol_to_chars, key=lambda symbol: symbol.name):
    for char in symbol_to_chars[symbol]:

        top_name = get_sprite_name(symbol, char, False)
        bottom_name = get_sprite_name(symbol, char, True)

        all_top_names.add(top_name)
        all_bottom_names.add(bottom_name)
        
        rules[top_name] = {
            "sprite": f"{RULE_NAME}/{top_name}.png",
            "weight": symbol.weight,
            "up": set(),
            "down": {bottom_name},
            "left": set(),
            "right": set(),
        }
        rules[bottom_name] = {
            "sprite": f"{RULE_NAME}/{bottom_name}.png",
            "weight": symbol.weight,
            "up": {top_name},
            "down": set(),
            "left": set(),
            "right": set(),
        }

# Add vertical connections
for top_name in all_top_names:
    rules[top_name]["up"] = all_bottom_names
for bottom_name in all_bottom_names:
    rules[bottom_name]["down"] = all_top_names



# Generate remaining connections
for phrase in PHRASES:
    for symbol_left, symbol_right in zip(phrase, phrase[1:]):
        for char_left in symbol_to_chars[symbol_left]:
            for char_right in symbol_to_chars[symbol_right]:
                for bottom in (False, True):
                    name_left = get_sprite_name(symbol_left, char_left, bottom)
                    name_right = get_sprite_name(symbol_right, char_right, bottom)

                    rules[name_right]["left"].add(name_left) # type: ignore
                    rules[name_left]["right"].add(name_right) # type: ignore



# Save the rules
for name in rules:
    for direction in ["up", "down", "left", "right"]:
        rules[name][direction] = sorted(rules[name][direction]) # type: ignore

with open(RULES_PATH, "w", encoding="utf-8") as f:
    json.dump(rules, f, indent=4)
