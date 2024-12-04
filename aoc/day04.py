from pathlib import Path

"""
DIRECTION REFERENCE

(-1,-1)(0,-1)(1, -1)
(-1, 0)(0, 0)(1, 0)
(-1, 1)(0, 1)(1,  1)
"""

XMAS_DIRECTIONS = {
    "north": ((complex(0, -1), "M"), (complex(0, -2), "A"), (complex(0, -3), "S")),
    "northeast": ((complex(1, -1), "M"), (complex(2, -2), "A"), (complex(3, -3), "S")),
    "east": ((complex(1, 0), "M"), (complex(2, 0), "A"), (complex(3, 0), "S")),
    "southeast": ((complex(1, 1), "M"), (complex(2, 2), "A"), (complex(3, 3), "S")),
    "south": ((complex(0, 1), "M"), (complex(0, 2), "A"), (complex(0, 3), "S")),
    "southwest": ((complex(-1, 1), "M"), (complex(-2, 2), "A"), (complex(-3, 3), "S")),
    "west": ((complex(-1, 0), "M"), (complex(-2, 0), "A"), (complex(-3, 0), "S")),
    "northwest": (
        (complex(-1, -1), "M"),
        (complex(-2, -2), "A"),
        (complex(-3, -3), "S"),
    ),
}

X_MAS_DIRECTIONS = {
    "north": (
        (complex(-1, -1), "M"),
        (complex(1, -1), "M"),
        (complex(-1, 1), "S"),
        (complex(1, 1), "S"),
    ),
    "east": (
        (complex(1, -1), "M"),
        (complex(1, 1), "M"),
        (complex(-1, 1), "S"),
        (complex(-1, -1), "S"),
    ),
    "south": (
        (complex(1, 1), "M"),
        (complex(-1, 1), "M"),
        (complex(-1, -1), "S"),
        (complex(1, -1), "S"),
    ),
    "west": (
        (complex(-1, -1), "M"),
        (complex(-1, 1), "M"),
        (complex(1, -1), "S"),
        (complex(1, 1), "S"),
    ),
}


def load_wordsearch(fp: Path) -> dict[complex, str]:
    result = {}
    with open(fp, "r") as f:
        for i, line in enumerate(f.readlines()):
            for j, char in enumerate(line):
                result[complex(j, i)] = char
    return result


def get_adjacent_count(
    start: complex,
    wordsearch: dict[complex, str],
    pattern: dict[str, tuple[tuple[complex, str], ...]],
) -> int:
    found = 0
    for cardinal, direction in pattern.items():
        if all(wordsearch.get(start + d) == c for d, c in direction):
            found += 1
    return found


def xmas_wordsearch(wordsearch: dict[complex, str]) -> int:
    found = 0
    for k, v in wordsearch.items():
        if v == "X":
            found += get_adjacent_count(k, wordsearch, XMAS_DIRECTIONS)
    return found


def x_mas_wordsearch(wordsearch: dict[complex, str]) -> int:
    found = 0
    for k, v in wordsearch.items():
        if v == "A":
            found += get_adjacent_count(k, wordsearch, X_MAS_DIRECTIONS)
    return found


def example_part_a():
    fp = Path("./example/day04-example-01.txt")
    wordsearch = load_wordsearch(fp)
    found = xmas_wordsearch(wordsearch)
    print(found, " == 4", sep="")  # 4

    fp = Path("./example/day04-example-02.txt")
    wordsearch = load_wordsearch(fp)
    found = xmas_wordsearch(wordsearch)
    print(found, " == 18", sep="")  # 18


def part_a():
    fp = Path("./data/day04.txt")
    wordsearch = load_wordsearch(fp)
    found = xmas_wordsearch(wordsearch)
    print(found)


def example_part_b():
    fp = Path("./example/day04-example-02.txt")
    wordsearch = load_wordsearch(fp)
    found = x_mas_wordsearch(wordsearch)
    print(found, " == 9", sep="")  # 9


def part_b():
    fp = Path("./data/day04.txt")
    wordsearch = load_wordsearch(fp)
    found = x_mas_wordsearch(wordsearch)
    print(found)


if __name__ == "__main__":
    example_part_a()
    example_part_b()
    part_a()
    part_b()
