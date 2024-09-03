from enum import Enum
import os
from PIL import Image
import random

class Direction(Enum):
    Up = '^'
    Down = 'v'
    Left = '<'
    Right = '>'

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





"""
class Tile(Enum):
    Sky = '.'
    Dirt = '#'
    Grass = '-'
    LeftWall = '{'
    RightWall = '}'
    TLC = '/'
    TRC = '\\'

RULES = {
    Tile.Sky: {
        Direction.Up: [Tile.Sky],
        Direction.Down: [Tile.Sky, Tile.Grass, Tile.TLC, Tile.TRC],
        Direction.Left: [Tile.Sky, Tile.RightWall, Tile.TRC],
        Direction.Right: [Tile.Sky, Tile.LeftWall, Tile.TLC],
    },
    Tile.Dirt: {
        Direction.Up: [Tile.Dirt, Tile.Grass],
        Direction.Down: [Tile.Dirt, Tile.Grass, Tile.TLC, Tile.TRC],
        Direction.Left: [Tile.Dirt, Tile.LeftWall, Tile.RightWall, Tile.TRC],
        Direction.Right: [Tile.Dirt, Tile.LeftWall, Tile.RightWall, Tile.TLC],
    },
    Tile.Grass: {
        Direction.Up: [Tile.Sky, Tile.Dirt, Tile.Grass, Tile.LeftWall, Tile.RightWall, Tile.TLC, Tile.TRC],
        Direction.Down: [Tile.Dirt, Tile.Grass, Tile.TLC, Tile.TRC],
        Direction.Left: [Tile.Grass, Tile.RightWall, Tile.TLC],
        Direction.Right: [Tile.Grass, Tile.LeftWall, Tile.TRC],
    },
    Tile.LeftWall: {
        Direction.Up: [Tile.LeftWall, Tile.TLC],
        Direction.Down: [Tile.Grass, Tile.LeftWall, Tile.TRC],
        Direction.Left: [Tile.Sky, Tile.Dirt, Tile.Grass, Tile.TLC],
        Direction.Right: [Tile.Dirt, Tile.RightWall],
    },
    Tile.RightWall: {
        Direction.Up: [Tile.RightWall, Tile.TRC],
        Direction.Down: [Tile.Grass, Tile.RightWall, Tile.TLC],
        Direction.Left: [Tile.Dirt, Tile.LeftWall],
        Direction.Right: [Tile.Sky, Tile.Dirt, Tile.Grass, Tile.TRC],
    },
    Tile.TLC: {
        Direction.Up: [Tile.Sky, Tile.Dirt, Tile.Grass, Tile.RightWall, Tile.TRC],
        Direction.Down: [Tile.Grass, Tile.LeftWall, Tile.TRC],
        Direction.Left: [Tile.Sky, Tile.Dirt],
        Direction.Right: [Tile.Grass, Tile.LeftWall, Tile.TRC],
    },
    Tile.TRC: {
        Direction.Up: [Tile.Sky, Tile.Dirt, Tile.Grass, Tile.LeftWall, Tile.TLC],
        Direction.Down: [Tile.Grass, Tile.RightWall, Tile.TLC],
        Direction.Left: [Tile.Grass, Tile.RightWall, Tile.TLC],
        Direction.Right: [Tile.Sky, Tile.Dirt],
    },
}
"""





class Tile(Enum):
    Board = ' '
    WireUD = '│'
    WireUL = '┘'
    WireUR = '└'
    WireDL = '┐'
    WireDR = '┌'
    WireLR = '─'
    WireUDL = '┤'
    WireUDR = '├'
    WireULR = '┴'
    WireDLR = '┬'
    WireUDLR = '┼'
    WireDiag = '╱'
    WireAntidiag = '╲'
    Chip = '█'
    ChipU = '┻'
    ChipD = '┳'
    ChipL = '┫'
    ChipR = '┣'
    ChipUL = '┏'
    ChipUR = '┓'
    ChipDL = '┗'
    ChipDR = '┛'
    PinU = '╽'
    PinD = '╿'
    PinL = '╼'
    PinR = '╾'

RULES = {
    Tile.Board: {
        Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR, Tile.PinL, Tile.PinR],
        Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR, Tile.PinL, Tile.PinR],
        Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL, Tile.PinU, Tile.PinD],
        Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR, Tile.PinU, Tile.PinD],
    },
    Tile.WireUD: {
        Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
        Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
        Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL, Tile.PinU, Tile.PinD],
        Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR, Tile.PinU, Tile.PinD],
    },
    Tile.WireUL: {
        Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
        Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR, Tile.PinL, Tile.PinR],
        Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
        Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR, Tile.PinU, Tile.PinD],
    },
    Tile.WireUR: {
        Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
        Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR, Tile.PinL, Tile.PinR],
        Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL, Tile.PinU, Tile.PinD],
        Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
    },
    Tile.WireDL: {
        Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR, Tile.PinL, Tile.PinR],
        Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
        Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
        Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR, Tile.PinU, Tile.PinD],
    },
    Tile.WireDR: {
        Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR, Tile.PinL, Tile.PinR],
        Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
        Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL, Tile.PinU, Tile.PinD],
        Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
    },
    Tile.WireLR: {
        Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR, Tile.PinL, Tile.PinR],
        Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR, Tile.PinL, Tile.PinR],
        Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
        Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
    },
    Tile.WireUDL: {
        Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
        Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
        Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
        Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR, Tile.PinU, Tile.PinD],
    },
    Tile.WireUDR: {
        Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
        Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
        Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL, Tile.PinU, Tile.PinD],
        Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
    },
    Tile.WireULR: {
        Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
        Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR, Tile.PinL, Tile.PinR],
        Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
        Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
    },
    Tile.WireDLR: {
        Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR, Tile.PinL, Tile.PinR],
        Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
        Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
        Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
    },
    Tile.WireUDLR: {
        Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
        Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
        Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
        Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
    },
    Tile.WireDiag: {
        Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
        Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
        Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
        Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
    },
    Tile.WireAntidiag: {
        Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
        Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
        Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
        Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
    },
    Tile.Chip: {
        Direction.Up: [Tile.Chip, Tile.ChipU],
        Direction.Down: [Tile.Chip, Tile.ChipD],
        Direction.Left: [Tile.Chip, Tile.ChipL],
        Direction.Right: [Tile.Chip, Tile.ChipR],
    },
    Tile.ChipU: {
        Direction.Up: [Tile.PinU],
        Direction.Down: [Tile.Chip],
        Direction.Left: [Tile.ChipU, Tile.ChipUL],
        Direction.Right: [Tile.ChipU, Tile.ChipUR],
    },
    Tile.ChipD: {
        Direction.Up: [Tile.Chip],
        Direction.Down: [Tile.PinD],
        Direction.Left: [Tile.ChipD, Tile.ChipDL],
        Direction.Right: [Tile.ChipD, Tile.ChipDR],
    },
    Tile.ChipL: {
        Direction.Up: [Tile.ChipL, Tile.ChipUL],
        Direction.Down: [Tile.ChipL, Tile.ChipDL],
        Direction.Left: [Tile.PinL],
        Direction.Right: [Tile.Chip],
    },
    Tile.ChipR: {
        Direction.Up: [Tile.ChipR, Tile.ChipUR],
        Direction.Down: [Tile.ChipR, Tile.ChipDR],
        Direction.Left: [Tile.Chip],
        Direction.Right: [Tile.PinR],
    },
    Tile.ChipUL: {
        Direction.Up: [Tile.PinU],
        Direction.Down: [Tile.ChipL, Tile.ChipDL],
        Direction.Left: [Tile.PinL],
        Direction.Right: [Tile.ChipU, Tile.ChipUR],
    },
    Tile.ChipUR: {
        Direction.Up: [Tile.PinU],
        Direction.Down: [Tile.ChipR, Tile.ChipDR],
        Direction.Left: [Tile.ChipU, Tile.ChipUL],
        Direction.Right: [Tile.PinR],
    },
    Tile.ChipDL: {
        Direction.Up: [Tile.ChipL, Tile.ChipUL],
        Direction.Down: [Tile.PinD],
        Direction.Left: [Tile.PinL],
        Direction.Right: [Tile.ChipD, Tile.ChipDR],
    },
    Tile.ChipDR: {
        Direction.Up: [Tile.ChipR, Tile.ChipUR],
        Direction.Down: [Tile.PinD],
        Direction.Left: [Tile.ChipD, Tile.ChipDL],
        Direction.Right: [Tile.PinR],
    },
    Tile.PinU: {
        Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
        Direction.Down: [Tile.ChipU, Tile.ChipUL, Tile.ChipUR],
        Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL, Tile.PinU],
        Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR, Tile.PinU],
    },
    Tile.PinD: {
        Direction.Up: [Tile.ChipD, Tile.ChipDL, Tile.ChipDR],
        Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
        Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL, Tile.PinD],
        Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR, Tile.PinD],
    },
    Tile.PinL: {
        Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR, Tile.PinL],
        Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR, Tile.PinL],
        Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
        Direction.Right: [Tile.ChipL, Tile.ChipUL, Tile.ChipDL],
    },
    Tile.PinR: {
        Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR, Tile.PinR],
        Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR, Tile.PinR],
        Direction.Left: [Tile.ChipR, Tile.ChipUR, Tile.ChipDR],
        Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
    },
}

### Backup ###
# RULES = {
#     Tile.Board: {
#         Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR],
#         Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR],
#         Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL],
#         Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR],
#     },
#     Tile.WireUD: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL],
#         Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR],
#     },
#     Tile.WireUL: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR],
#     },
#     Tile.WireUR: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR],
#         Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#     },
#     Tile.WireDL: {
#         Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR],
#     },
#     Tile.WireDR: {
#         Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#     },
#     Tile.WireLR: {
#         Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR],
#         Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#     },
#     Tile.WireUDL: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR],
#     },
#     Tile.WireUDR: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#     },
#     Tile.WireULR: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#     },
#     Tile.WireDLR: {
#         Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#     },
#     Tile.WireUDLR: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#     },
#     Tile.WireDiag: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#     },
#     Tile.WireAntidiag: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.Pin],
#     },
# }

### Backup 2 ###
# RULES = {
#     Tile.Board: {
#         Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR],
#         Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR],
#         Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL],
#         Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR],
#     },
#     Tile.WireUD: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
#         Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL],
#         Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR],
#     },
#     Tile.WireUL: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
#         Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
#         Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR],
#     },
#     Tile.WireUR: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
#         Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR],
#         Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
#     },
#     Tile.WireDL: {
#         Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
#         Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR],
#     },
#     Tile.WireDR: {
#         Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
#         Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
#     },
#     Tile.WireLR: {
#         Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR],
#         Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
#     },
#     Tile.WireUDL: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
#         Direction.Right: [Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR],
#     },
#     Tile.WireUDR: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
#         Direction.Left: [Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
#     },
#     Tile.WireULR: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
#         Direction.Down: [Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
#     },
#     Tile.WireDLR: {
#         Direction.Up: [Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
#     },
#     Tile.WireUDLR: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
#     },
#     Tile.WireDiag: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
#     },
#     Tile.WireAntidiag: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
#     },
#     Tile.Chip: {
#         Direction.Up: [Tile.Chip, Tile.ChipU],
#         Direction.Down: [Tile.Chip, Tile.ChipD],
#         Direction.Left: [Tile.Chip, Tile.ChipL],
#         Direction.Right: [Tile.Chip, Tile.ChipR],
#     },
#     Tile.ChipU: {
#         Direction.Up: [Tile.PinU],
#         Direction.Down: [Tile.Chip],
#         Direction.Left: [Tile.ChipU, Tile.ChipUL],
#         Direction.Right: [Tile.ChipU, Tile.ChipUR],
#     },
#     Tile.ChipD: {
#         Direction.Up: [Tile.Chip],
#         Direction.Down: [Tile.PinD],
#         Direction.Left: [Tile.ChipD, Tile.ChipDL],
#         Direction.Right: [Tile.ChipD, Tile.ChipDR],
#     },
#     Tile.ChipL: {
#         Direction.Up: [Tile.ChipL, Tile.ChipUL],
#         Direction.Down: [Tile.ChipL, Tile.ChipDL],
#         Direction.Left: [Tile.PinL],
#         Direction.Right: [Tile.Chip],
#     },
#     Tile.ChipR: {
#         Direction.Up: [Tile.ChipR, Tile.ChipUR],
#         Direction.Down: [Tile.ChipR, Tile.ChipDR],
#         Direction.Left: [Tile.Chip],
#         Direction.Right: [Tile.PinR],
#     },
#     Tile.ChipUL: {
#         Direction.Up: [Tile.PinU],
#         Direction.Down: [Tile.ChipL, Tile.ChipDL],
#         Direction.Left: [Tile.PinL],
#         Direction.Right: [Tile.ChipU, Tile.ChipUR],
#     },
#     Tile.ChipUR: {
#         Direction.Up: [Tile.PinU],
#         Direction.Down: [Tile.ChipR, Tile.ChipDR],
#         Direction.Left: [Tile.ChipU, Tile.ChipUL],
#         Direction.Right: [Tile.PinR],
#     },
#     Tile.ChipDL: {
#         Direction.Up: [Tile.ChipL, Tile.ChipUL],
#         Direction.Down: [Tile.PinD],
#         Direction.Left: [Tile.PinL],
#         Direction.Right: [Tile.ChipD, Tile.ChipDR],
#     },
#     Tile.ChipDR: {
#         Direction.Up: [Tile.ChipR, Tile.ChipUR],
#         Direction.Down: [Tile.PinD],
#         Direction.Left: [Tile.ChipD, Tile.ChipDL],
#         Direction.Right: [Tile.PinR],
#     },
#     Tile.PinU: {
#         Direction.Up: [Tile.WireUD, Tile.WireDL, Tile.WireDR, Tile.WireUDL, Tile.WireUDR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinU],
#         Direction.Down: [Tile.ChipU, Tile.ChipUL, Tile.ChipUR],
#         Direction.Left: [Tile.PinU, Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL],
#         Direction.Right: [Tile.PinU, Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR],
#     },
#     Tile.PinD: {
#         Direction.Up: [Tile.ChipD, Tile.ChipDL, Tile.ChipDR],
#         Direction.Down: [Tile.WireUD, Tile.WireUL, Tile.WireUR, Tile.WireUDL, Tile.WireUDR, Tile.WireULR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinD],
#         Direction.Left: [Tile.PinD, Tile.Board, Tile.WireUD, Tile.WireUL, Tile.WireDL, Tile.WireUDL],
#         Direction.Right: [Tile.PinD, Tile.Board, Tile.WireUD, Tile.WireUR, Tile.WireDR, Tile.WireUDR],
#     },
#     Tile.PinL: {
#         Direction.Up: [Tile.PinL, Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR],
#         Direction.Down: [Tile.PinL, Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR],
#         Direction.Left: [Tile.WireUR, Tile.WireDR, Tile.WireLR, Tile.WireUDR, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinL],
#         Direction.Right: [Tile.ChipL, Tile.ChipUL, Tile.ChipDL],
#     },
#     Tile.PinR: {
#         Direction.Up: [Tile.PinR, Tile.Board, Tile.WireUL, Tile.WireUR, Tile.WireLR, Tile.WireULR],
#         Direction.Down: [Tile.PinR, Tile.Board, Tile.WireDL, Tile.WireDR, Tile.WireLR, Tile.WireDLR],
#         Direction.Left: [Tile.ChipR, Tile.ChipUR, Tile.ChipDR],
#         Direction.Right: [Tile.WireUL, Tile.WireDL, Tile.WireLR, Tile.WireUDL, Tile.WireULR, Tile.WireDLR, Tile.WireUDLR, Tile.WireDiag, Tile.WireAntidiag, Tile.PinR],
#     },
# }





Rules = dict[Tile, dict[Direction, list[Tile]]]

class WFC:
    def __init__(self, width: int, height: int, rules: Rules) -> None:
        self.width = width
        self.height = height
        self.rules = rules
        self.reset()
    
    def reset(self) -> None:
        self.grid = [
            [
                set(Tile)
                for _ in range(self.width)
            ]
            for _ in range(self.height)
        ]

    def verify_rules(self, early_stop: bool = False) -> bool:
        error = False
        
        # Check for tile
        for tile in Tile:
            if tile not in self.rules:
                print(f"Tile {tile.name} not found in the rules")
                if early_stop:
                    return False
                error = True
        
        # Check for direction
        for tile in Tile:
            for direction in Direction:
                if direction not in self.rules[tile]:
                    print(f"Direction {direction.name} missing in the rules for tile {tile.name}")
                    if early_stop:
                        return False
                    error = True
                
        # Check for overlap
        for tile in Tile:
            for direction in Direction:
                for tile2 in self.rules[tile][direction]:
                    if tile not in self.rules[tile2][direction.opposite]:
                        print(f"Tile {tile2.name} found for {tile.name}:{direction.name} but not the other way around")
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
        remaining = self.get_not_collapsed()
        if not remaining:
            return None

        i, j = random.choice(remaining)
        selected = random.choice(sorted(self.grid[i][j], key=lambda t: t.name)) # Sorting ensures reproduciability
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
            self.debug()
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

            # TEMP
            print(self)
            print()

            if all(all(len(states) == 1 for states in row) for row in self.grid):
                break
        
        return [[list(states)[0] for states in row] for row in self.grid]

    # TEMP
    def debug(self):
        self._debug = [
            [
                ''.join(state.value for state in states)
                for states in row
            ]
            for row in self.grid
        ]

    def to_image(self, image_dir: str) -> Image.Image:
        sprites = {
            tile: Image.open(
                os.path.join(image_dir, f"{i}.png")
            ).convert("RGBA")
            for i, tile in enumerate(Tile)
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
        return "\n".join(
            "".join(
                '+' if len(states) >= 10
                else list(states)[0].value if len(states) == 1
                else str(len(states))
                for states in row
            )
            for row in self.grid
        )



# Very dangerous. Duplicates any mistake.
def generate_rule_symetry(rules: Rules) -> Rules:
    symmetry = {tile: {direction: set() for direction in Direction} for tile in Tile}

    for tile, rule in rules.items():
        for direction, allowed in rule.items():
            for tile2 in allowed:
                symmetry[tile][direction].add(tile2)
                symmetry[tile2][direction.opposite].add(tile)
    
    return {
        tile: {
            direction: sorted(
                symmetry[tile][direction],
                key=lambda tile: list(Tile).index(tile)
            ) 
            for direction in Direction
        }
        for tile in Tile
    }

def rules_to_str(rules: Rules) -> str:
    L = ["{"]

    for tile in Tile:
        L.append(f"    Tile.{tile.name}: {{")
        for direction in Direction:
            line = f"        Direction.{direction.name}: ["

            L2 = []
            for tile2 in sorted(
                rules.get(tile, {}).get(direction, []),
                key=lambda tile: list(Tile).index(tile)
            ):
                L2.append(f"Tile.{tile2.name}")

            line += ", ".join(L2)
            L.append(line + "],")
        L.append("    },")

    L.append("}")
    return "\n".join(L)



def main() -> None:
    random.seed(0) # TEMP
    import clipboard # TEMP
    # RULES = generate_rule_symetry(RULES) # TEMP
    # clipboard.copy(rules_to_str(RULES)) # TEMP

    WIDTH, HEIGHT = 30, 30
    wfc = WFC(WIDTH, HEIGHT, RULES)
    if not wfc.verify_rules():
        return

    wfc.generate()
    wfc.to_image("images").show()

if __name__ == "__main__":
    main()
