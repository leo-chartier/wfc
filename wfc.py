import argparse
from enum import Enum
import json
import sys
from jsonschema import validate
import os
from PIL import Image
import random
from typing import TextIO

class Direction(Enum):
    Up = 'up'
    Down = 'down'
    Left = 'left'
    Right = 'right'

    @property
    def opposite(self) -> "Direction":
        match self:
            case Direction.Up:
                return Direction.Down
            case Direction.Down:
                return Direction.Up
            case Direction.Left:
                return Direction.Right
            case Direction.Right:
                return Direction.Left

    @property
    def offset(self) -> tuple[int, int]:
        match self:
            case Direction.Up:
                return (-1, 0)
            case Direction.Down:
                return (1, 0)
            case Direction.Left:
                return (0, -1)
            case Direction.Right:
                return (0, 1)

Tile = str

Rules = dict[Tile, dict[Direction, list[Tile]]]
Meta = dict[str, dict[Tile, str | int]]

class WFC:
    def __init__(self, width: int, height: int, tiles: list[Tile], rules: Rules, meta: Meta | None = None, use_minimal_entropy: bool = True) -> None:
        self.width = width
        self.height = height
        self.tiles = sorted(tiles)
        self.rules = rules
        self.meta = meta or {}
        self.use_minimal_entropy = use_minimal_entropy
        self.reset()
    
    def reset(self) -> None:
        valid = set(self.tiles)
        for tile in self.tiles:
            if self.meta.get("weight", {}).get(tile, 1) <= 0: # type: ignore
                valid.remove(tile)
        self.grid = [
            [
                valid.copy()
                for _ in range(self.width)
            ]
            for _ in range(self.height)
        ]
    
    @staticmethod
    def from_json(f: TextIO, width: int, height: int, use_minimal_entropy: bool = True) -> "WFC":
        j = json.load(f)

        with open("schema.json", "r") as sf:
            schema = json.load(sf)
            validate(j, schema)

        rules: Rules = {}
        meta: Meta = {
            "symbol": {},
            "sprite": {},
            "weight": {},
        }

        for tile, rule in j.items():
            rules[tile] = {}

            for key, value in rule.items():
                match key:
                    case "symbol" | "sprite" | "weight":
                        meta[key][tile] = value
                    case "up" | "down" | "left" | "right":
                        direction: Direction = Direction._value2member_map_[key] # type: ignore
                        rules[tile][direction] = value
                    case _:
                        raise KeyError(f"Invalid rule file: Key {key} is invalid for tile {tile}")
        
        tiles = get_tiles_from_rules(rules)

        meta = {k: v for k, v in meta.items() if v}

        return WFC(width, height, tiles, rules, meta, use_minimal_entropy)

    def verify_rules(self, early_stop: bool = False) -> bool:
        error = False
        
        # Check for tile
        for tile in self.tiles:
            if tile not in self.rules:
                print(f"Tile {tile} not found in the rules")
                if early_stop:
                    return False
                error = True
        
        # Check for direction
        for tile in self.tiles:
            for direction in Direction:
                if direction not in self.rules[tile]:
                    print(f"Direction {direction.name} missing in the rules for tile {tile}")
                    if early_stop:
                        return False
                    error = True
                
        # Check for overlap
        for tile in self.tiles:
            for direction in Direction:
                for tile2 in self.rules[tile][direction]:
                    if tile not in self.rules[tile2][direction.opposite]:
                        print(f"Tile {tile2} found for {tile}:{direction.name} but not the other way around")
                        if early_stop:
                            return False
                        error = True

        return not error
    
    def get_not_collapsed(self) -> list[tuple[int, int]]:
        return [
            (i, j)
            for i in range(self.height)
            for j in range(self.height)
            if len(self.grid[i][j]) > 1
        ]
    
    def collapse(self) -> tuple[int, int] | None:
        possibilities = self.get_not_collapsed()

        if self.use_minimal_entropy and possibilities:
            min_entropy = min(len(states) for row in self.grid for states in row if len(states) > 1)
            possibilities = [(i, j) for i, j in possibilities if len(self.grid[i][j]) == min_entropy]
        
        if not possibilities:
            return None

        i, j = random.choice(possibilities)
        weighted_states = [
            tile
            for tile in sorted(self.grid[i][j]) # Sorting ensures reproducibility
            for _ in range(self.meta["weight"].get(tile, 1)) # type: ignore
        ]
        selected = random.choice(weighted_states)
        self.grid[i][j] = {selected}

        return i, j

    def propagate(self, i: int, j: int) -> list[tuple[int, int]]:
        if i not in range(self.height) or j not in range(self.width):
            return []

        changed: list[tuple[int, int]] = []
        valid = set(self.grid[i][j])

        for direction in Direction:
            di, dj = direction.offset
            i2, j2 = i + di, j + dj
            if i2 not in range(self.height) or j2 not in range(self.width):
                continue

            for state in self.grid[i2][j2].copy():
                required = self.rules[state][direction.opposite]
                if not valid.intersection(required):
                    self.grid[i2][j2].remove(state)
                    changed.append((i2, j2))

        return changed

    def step(self) -> bool:
        coords = self.collapse()
        if coords is None:
            return False

        remaining = [coords]
        while remaining:
            i, j = remaining.pop()

            if len(self.grid[i][j]) == 0:
                return False

            remaining += self.propagate(i, j)
        
        return True

    def run(self) -> None:
        while self.step():
            continue
    
    def generate(self) -> list[list[Tile]]:
        while True:
            self.reset()
            self.run()

            if all(all(len(states) == 1 for states in row) for row in self.grid):
                break
        
        return [[list(states)[0] for states in row] for row in self.grid]

    def to_image(self) -> Image.Image | None:
        if "sprite" not in self.meta:
            return None

        sprites = {
            tile: Image.open(
                os.path.join(self.meta["sprite"][tile]) # type: ignore
            ).convert("RGBA")
            for tile in self.tiles
        }
        
        w, h = list(sprites.values())[0].size
        if not all(sprite.width == w and sprite.height == h for sprite in sprites.values()):
            raise ValueError("All the images must have the same size")

        img = Image.new("RGBA", (w * self.width, h * self.height))

        for i, row in enumerate(self.grid):
            for j, states in enumerate(row):
                if len(states) != 1:
                    continue

                state = list(states)[0]
                img.paste(sprites[state], (j * w, i * h))
        
        return img

    def __repr__(self) -> str:
        if "symbol" not in self.meta:
            return super().__repr__()
        
        def get_symbol(states: set[Tile]) -> str:
            if len(states) >= 10:
                return '?'
            if len(states) != 1:
                return str(len(states))
            state = list(states)[0]
            return self.meta["symbol"].get(state, '?') # type: ignore

        return "\n".join(
            "".join(
                get_symbol(states)
                for states in row
            )
            for row in self.grid
        )



def get_tiles_from_rules(rules: Rules) -> list[Tile]:
    tiles = set(rules)
    for rule in rules.values():
        for allowed in rule.values():
            tiles.update(allowed)
    return sorted(tiles)

# Very dangerous. Duplicates any mistake.
def generate_rule_symetry(rules: Rules) -> Rules:
    tiles = get_tiles_from_rules(rules)
    symmetry = {tile: {direction: set() for direction in Direction} for tile in tiles}

    for tile, rule in rules.items():
        for direction, allowed in rule.items():
            for tile2 in allowed:
                symmetry[tile][direction].add(tile2)
                symmetry[tile2][direction.opposite].add(tile)
    
    return {
        tile: {
            direction: sorted(
                symmetry[tile][direction],
                key=lambda tile: tiles.index(tile)
            ) 
            for direction in Direction
        }
        for tile in tiles
    }



def main() -> None:
    def strictly_positive(arg: str) -> int:
        try:
            v = int(arg)
        except ValueError:
            raise argparse.ArgumentTypeError("Size must be an integer")
        
        if v <= 0:
            raise argparse.ArgumentTypeError("Size must be strictly positive")
        
        return v

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "fp",
        metavar="filename",
        help="name of the file containing the rules",
    )
    parser.add_argument(
        "width",
        help="width of the output image in tiles",
        type=strictly_positive,
    )
    parser.add_argument(
        "height",
        help="height of the output image in tiles",
        type=strictly_positive,
    )
    parser.add_argument(
        "--seed",
        help="seed for the randomizer",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--no-min-entropy",
        help="disables the selection by minimal entropy",
        action="store_false",
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    sys.stdout.reconfigure(encoding='utf-8') # type: ignore
    with open(args.fp, "r", encoding="utf-8") as f:
        wfc = WFC.from_json(f, args.width, args.height, args.no_min_entropy)
    
    if not wfc.verify_rules():
        return

    wfc.generate()
    print(wfc)

    img = wfc.to_image()
    if img is not None:
        img.show()

if __name__ == "__main__":
    main()
