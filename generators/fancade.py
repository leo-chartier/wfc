from enum import Enum, auto
import json
import os
from typing import Generator

RULES_PATH = os.path.join(os.path.dirname(__file__), '..', 'rules', 'fancade.json')

class Tile(Enum):
    # In order in my tileset
    If = auto()
    Play = auto()
    Loop = auto()
    Touch = auto()
    BreakVec = auto()
    MakeVec = auto()
    And = auto()
    Camera = auto()
    SetLocation = auto()
    Raycast = auto()
    Not = auto()
    GetLocation = auto()
    Create = auto()
    Delete = auto()
    PlaySound = auto()
    Or = auto()
    AddNum = auto()
    AddVec = auto()
    SubNum = auto()
    SubVec = auto()
    Multiply = auto()
    Modulo = auto()
    Win = auto()
    Lose = auto()
    EqualNum = auto()
    EqualVec = auto()
    EqualObject = auto()
    LessThan = auto()
    GreaterThan = auto()
    Distance = auto()
    ScreenToWorld = auto()
    WorldToScreen = auto()
    Random = auto()
    Min = auto()
    Max = auto()
    Round = auto()
    Floor = auto()
EMPTY = 'Empty'

class WireType(Enum):
    Number = 'N'
    Vector = 'V'
    Rotation = 'R'
    Bool = 'B'
    Object = 'O'
    Execution = 'E'
NO_CONNECTION = '-'

FORCE_WIRE = True



DEFAULT_HEIGHT = 2
HEIGHTS  = {
    Tile.Touch: 3,
    Tile.BreakVec: 3,
    Tile.MakeVec: 3,
    Tile.Camera: 3,
    Tile.SetLocation: 3,
    Tile.Raycast: 3,
    Tile.Not: 1,
    Tile.Round: 1,
    Tile.Floor: 1,
}

INPUTS = {
    Tile.If: [WireType.Bool],
    Tile.Loop: [WireType.Number, WireType.Number],
    Tile.BreakVec: [WireType.Vector],
    Tile.MakeVec: [WireType.Number, WireType.Number, WireType.Number],
    Tile.And: [WireType.Bool, WireType.Bool],
    Tile.Camera: [WireType.Vector, WireType.Rotation, WireType.Number],
    Tile.SetLocation: [WireType.Object, WireType.Vector, WireType.Rotation],
    Tile.Raycast: [WireType.Vector, WireType.Vector],
    Tile.Not: [WireType.Bool],
    Tile.GetLocation: [WireType.Object],
    Tile.Create: [WireType.Object],
    Tile.Delete: [WireType.Object],
    Tile.PlaySound: [WireType.Number, WireType.Number],
    Tile.Or: [WireType.Bool],
    Tile.AddNum: [WireType.Number, WireType.Number],
    Tile.AddVec: [WireType.Vector, WireType.Vector],
    Tile.SubNum: [WireType.Number, WireType.Number],
    Tile.SubVec: [WireType.Vector, WireType.Vector],
    Tile.Multiply: [WireType.Number, WireType.Number],
    Tile.Modulo: [WireType.Number, WireType.Number],
    Tile.EqualNum: [WireType.Number, WireType.Number],
    Tile.EqualVec: [WireType.Vector, WireType.Vector],
    Tile.EqualObject: [WireType.Object, WireType.Object],
    Tile.LessThan: [WireType.Number, WireType.Number],
    Tile.GreaterThan: [WireType.Number, WireType.Number],
    Tile.Distance: [WireType.Vector, WireType.Vector],
    Tile.ScreenToWorld: [WireType.Number, WireType.Number],
    Tile.WorldToScreen: [WireType.Vector, WireType.Vector],
    Tile.Random: [WireType.Number, WireType.Number],
    Tile.Min: [WireType.Number, WireType.Number],
    Tile.Max: [WireType.Number, WireType.Number],
    Tile.Round: [WireType.Number],
    Tile.Floor: [WireType.Number],
}

OUTPUTS = {
    Tile.If: [WireType.Execution, WireType.Execution],
    Tile.Play: [WireType.Execution],
    Tile.Loop: [WireType.Execution, WireType.Number],
    Tile.Touch: [WireType.Execution, WireType.Number, WireType.Number],
    Tile.BreakVec: [WireType.Number, WireType.Number, WireType.Number],
    Tile.MakeVec: [WireType.Vector],
    Tile.And: [WireType.Bool],
    Tile.Raycast: [WireType.Bool, WireType.Vector, WireType.Object],
    Tile.Not: [WireType.Bool],
    Tile.GetLocation: [WireType.Vector, WireType.Rotation],
    Tile.Create: [WireType.Object],
    Tile.PlaySound: [WireType.Number],
    Tile.Or: [WireType.Bool],
    Tile.AddNum: [WireType.Number],
    Tile.AddVec: [WireType.Vector],
    Tile.SubNum: [WireType.Number],
    Tile.SubVec: [WireType.Vector],
    Tile.Multiply: [WireType.Number],
    Tile.Modulo: [WireType.Number],
    Tile.EqualNum: [WireType.Bool],
    Tile.EqualVec: [WireType.Bool],
    Tile.EqualObject: [WireType.Bool],
    Tile.LessThan: [WireType.Bool],
    Tile.GreaterThan: [WireType.Bool],
    Tile.Distance: [WireType.Number],
    Tile.ScreenToWorld: [WireType.Vector, WireType.Vector],
    Tile.WorldToScreen: [WireType.Number, WireType.Number],
    Tile.Random: [WireType.Number],
    Tile.Min: [WireType.Number],
    Tile.Max: [WireType.Number],
    Tile.Round: [WireType.Number],
    Tile.Floor: [WireType.Number],
}

HAS_EXEC = [
    Tile.If,
    Tile.Play,
    Tile.Loop,
    Tile.Touch,
    Tile.Camera,
    Tile.SetLocation,
    Tile.Create,
    Tile.Delete,
    Tile.PlaySound,
    Tile.Win,
    Tile.Lose,
]



left_right: list[tuple[str, str]] = [(EMPTY, EMPTY)]
up_down: list[tuple[str, str]] = [(EMPTY, EMPTY)]
tiles_names: set[str] = {EMPTY}

def get_connection(tile: Tile, line: int, right_side: bool) -> WireType | None:
    _map = OUTPUTS if right_side else INPUTS
    connections = _map.get(tile, [])
    return connections[line] if line < len(connections) else None

def names_generator(tile: Tile, line: int, right_side: bool) -> Generator[str, None, None]:
    connections = {get_connection(tile, line, right_side)}
    if not FORCE_WIRE:
        connections.add(None)
    has_exec = not right_side and tile in HAS_EXEC

    for connection in connections:
        left = connection.value if not right_side and connection else NO_CONNECTION
        right = connection.value if right_side and connection else NO_CONNECTION
        up = WireType.Execution.value if has_exec and line == 0 else NO_CONNECTION
        down = WireType.Execution.value if has_exec and line + 1 == HEIGHTS.get(tile, DEFAULT_HEIGHT) else NO_CONNECTION
        name = f"{tile.name}_{line+1}{'R' if right_side else 'L'}_{up}{right}{down}{left}"
        yield name

# Generate connections between pieces
for tile in Tile:
    height = HEIGHTS.get(tile, DEFAULT_HEIGHT)
    for j in range(height):
        for left in names_generator(tile, j, False):
            for right in names_generator(tile, j, True):
                tiles_names.add(left)
                tiles_names.add(right)
                left_right.append((left, right))
    for j in range(height - 1):
        for side in (False, True):
            for up in names_generator(tile, j, side):
                for down in names_generator(tile, j + 1, side):
                    up_down.append((up, down))

# Generate connections with empty tiles
for tile in Tile:
    height = HEIGHTS.get(tile, DEFAULT_HEIGHT)
    for j in range(height):
        for left in names_generator(tile, j, False):
            left_right.append((EMPTY, left))
        for right in names_generator(tile, j, True):
            left_right.append((right, EMPTY))
    for side in range(2):
        for up in names_generator(tile, 0, bool(side)):
            up_down.append((EMPTY, up))
        for down in names_generator(tile, height-1, bool(side)):
            up_down.append((down, EMPTY))



def name_to_sprite(name: str) -> str:
    # The name of the sprite is the same as the one of the tile except
    # that the connections down and to the left do not change so they
    # are removed
    if name.count('_') < 2:
        # It's air or a connection
        return name
    # It's a tile
    return name[:-2]

# Generate the rule file
rules = {}

for name in sorted(tiles_names):
    sprite_name = name_to_sprite(name)
    up = sorted(set(up for up, down in up_down if down == name))
    down = sorted(set(down for up, down in up_down if up == name))
    left = sorted(set(left for left, right in left_right if right == name))
    right = sorted(set(right for left, right in left_right if left == name))
    rule = {
        # TODO: Symbol
        'sprite': f'sprites/fancade/{sprite_name}.png',
        'up': up,
        'down': down,
        'left': left,
        'right': right,
    }
    rules[name] = rule

# Make it 50% empty
rules[EMPTY]['weight'] = len(tiles_names)

with open(RULES_PATH, 'w', encoding='utf-8') as f:
    json.dump(rules, f, indent=4)