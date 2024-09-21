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

class Connection(Enum):
    Number = 'N'
    Vector = 'V'
    Rotation = 'R'
    Bool = 'B'
    Object = 'O'
    Execution = 'E'
NO_CONNECTION = '-'



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
    Tile.If: [Connection.Bool],
    Tile.Loop: [Connection.Number, Connection.Number],
    Tile.BreakVec: [Connection.Vector],
    Tile.MakeVec: [Connection.Number, Connection.Number, Connection.Number],
    Tile.And: [Connection.Bool, Connection.Bool],
    Tile.Camera: [Connection.Vector, Connection.Rotation, Connection.Number],
    Tile.SetLocation: [Connection.Object, Connection.Vector, Connection.Rotation],
    Tile.Raycast: [Connection.Vector, Connection.Vector],
    Tile.Not: [Connection.Bool],
    Tile.GetLocation: [Connection.Object],
    Tile.Create: [Connection.Object],
    Tile.Delete: [Connection.Object],
    Tile.PlaySound: [Connection.Number, Connection.Number],
    Tile.Or: [Connection.Bool],
    Tile.AddNum: [Connection.Number, Connection.Number],
    Tile.AddVec: [Connection.Vector, Connection.Vector],
    Tile.SubNum: [Connection.Number, Connection.Number],
    Tile.SubVec: [Connection.Vector, Connection.Vector],
    Tile.Multiply: [Connection.Number, Connection.Number],
    Tile.Modulo: [Connection.Number, Connection.Number],
    Tile.EqualNum: [Connection.Number, Connection.Number],
    Tile.EqualVec: [Connection.Vector, Connection.Vector],
    Tile.EqualObject: [Connection.Object, Connection.Object],
    Tile.LessThan: [Connection.Number, Connection.Number],
    Tile.GreaterThan: [Connection.Number, Connection.Number],
    Tile.Distance: [Connection.Vector, Connection.Vector],
    Tile.ScreenToWorld: [Connection.Number, Connection.Number],
    Tile.WorldToScreen: [Connection.Vector, Connection.Vector],
    Tile.Random: [Connection.Number, Connection.Number],
    Tile.Min: [Connection.Number, Connection.Number],
    Tile.Max: [Connection.Number, Connection.Number],
    Tile.Round: [Connection.Number],
    Tile.Floor: [Connection.Number],
}

OUTPUTS = {
    Tile.If: [Connection.Execution, Connection.Execution],
    Tile.Play: [Connection.Execution],
    Tile.Loop: [Connection.Execution, Connection.Number],
    Tile.Touch: [Connection.Execution, Connection.Number, Connection.Number],
    Tile.BreakVec: [Connection.Number, Connection.Number, Connection.Number],
    Tile.MakeVec: [Connection.Vector],
    Tile.And: [Connection.Bool],
    Tile.Raycast: [Connection.Bool, Connection.Vector, Connection.Object],
    Tile.Not: [Connection.Bool],
    Tile.GetLocation: [Connection.Vector, Connection.Rotation],
    Tile.Create: [Connection.Object],
    Tile.PlaySound: [Connection.Number],
    Tile.Or: [Connection.Bool],
    Tile.AddNum: [Connection.Number],
    Tile.AddVec: [Connection.Vector],
    Tile.SubNum: [Connection.Number],
    Tile.SubVec: [Connection.Vector],
    Tile.Multiply: [Connection.Number],
    Tile.Modulo: [Connection.Number],
    Tile.EqualNum: [Connection.Bool],
    Tile.EqualVec: [Connection.Bool],
    Tile.EqualObject: [Connection.Bool],
    Tile.LessThan: [Connection.Bool],
    Tile.GreaterThan: [Connection.Bool],
    Tile.Distance: [Connection.Number],
    Tile.ScreenToWorld: [Connection.Vector, Connection.Vector],
    Tile.WorldToScreen: [Connection.Number, Connection.Number],
    Tile.Random: [Connection.Number],
    Tile.Min: [Connection.Number],
    Tile.Max: [Connection.Number],
    Tile.Round: [Connection.Number],
    Tile.Floor: [Connection.Number],
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



left_right: list[tuple[str, str]] = []
up_down: list[tuple[str, str]] = []
tiles_names: set[str] = {EMPTY}

def get_connection(tile: Tile, line: int, right_side: bool) -> Connection | None:
    _map = OUTPUTS if right_side else INPUTS
    connections = _map.get(tile, [])
    return connections[line] if line < len(connections) else None

def names_generator(tile: Tile, line: int, right_side: bool) -> Generator[str, None, None]:
    connections = {get_connection(tile, line, right_side)}
    connections.add(None)
    has_exec = not right_side and tile in HAS_EXEC

    for connection in connections:
        left = connection.value if not right_side and connection else NO_CONNECTION
        right = connection.value if right_side and connection else NO_CONNECTION
        up = Connection.Execution.value if has_exec and line == 0 else NO_CONNECTION
        down = Connection.Execution.value if has_exec and line + 1 == HEIGHTS.get(tile, DEFAULT_HEIGHT) else NO_CONNECTION
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
    left = sorted(set(left for left, right in up_down if right == name))
    right = sorted(set(right for left, right in up_down if left == name))
    rule = {
        # TODO: Symbol
        'sprite': f'sprites/fancade/{sprite_name}.png',
        'up': up,
        'down': down,
        'left': left,
        'right': right,
    }
    rules[name] = rule

with open(RULES_PATH, 'w', encoding='utf-8') as f:
    json.dump(rules, f, indent=4)