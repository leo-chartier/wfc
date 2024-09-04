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



# Remove old sprites if any
if os.path.isdir(SPRITE_DIR_PATH):
    shutil.rmtree(SPRITE_DIR_PATH)
os.mkdir(SPRITE_DIR_PATH)

# Generate the sprites
for symbol in Symbol:
    for char, mask in char_to_mask.items():
        if not re.match(symbol.pattern, char):
            continue

        color = Image.new("RGB", mask.size, COLORS[symbol.token])
        sprite = Image.new("RGB", mask.size, BACKGROUND)
        sprite.paste(color, mask=mask)

        fn = f"{symbol.name}_{ord(char)}"
        sprite.crop(TOP_CROP).save(os.path.join(SPRITE_DIR_PATH, fn + ".png"))
        sprite.crop(BOTTOM_CROP).save(os.path.join(SPRITE_DIR_PATH, fn + "_.png"))



# Generate the rules
# TODO