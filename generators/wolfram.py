import json

# Ask user for rule number
code = int(input("Wolfram code [0-255]: "))
assert code in range(256)

# Generate ruleset
ruleset = {
    tuple(bool(i & j) for j in (1, 2, 4)): bool((1 << i) & code)
    for i in range(8)
}

# Name of the tile reflects the states of the tiles above
def to_name(p: bool, q: bool, r: bool) -> str:
    return f"{p*1}{q*1}{r*1}" + " #"[ruleset[(p, q, r)]]

# Generate the rules
rules = {}
for (p, q, r), s in ruleset.items():
    name = to_name(p, q, r)
    up = []
    down = []
    left = []
    right = []

    # Find the neighbors
    for (p2, q2, r2), s2 in ruleset.items():
        name2 = to_name(p2, q2, r2)
        if s2 == q:
            up.append(name2)
        if q2 == s:
            down.append(name2)
        if q2 == r and p2 == q:
            left.append(name2)
        if q2 == p and r2 == q:
            right.append(name2)

    rules[name] = {
        "symbol": " #"[s],
        "sprite": "black.png" if s else "white.png",
        "up": up,
        "down": down,
        "left": left,
        "right": right
    }

# Save the rules
with open(f"rule{code}.json", "w") as f:
    json.dump(rules, f, indent=4)