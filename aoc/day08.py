from collections import defaultdict
from dataclasses import dataclass
from itertools import permutations


@dataclass
class Bounds:
    x_min: int
    x_max: int
    y_min: int
    y_max: int

    def in_bounds(self, coordinate: complex) -> bool:
        return (
            self.x_min <= coordinate.real < self.x_max
            and self.y_min <= coordinate.imag < self.y_max
        )


def parse_data(fp) -> tuple[dict[str, set[complex]], Bounds]:
    data = defaultdict(set)
    with open(fp, "r") as f:
        rows = f.readlines()
    for y, row in enumerate(rows):
        for x, col in enumerate(row.strip()):
            if col != ".":
                data[col].add(complex(x, y))
    bounds = Bounds(0, len(rows[0].strip()), 0, len(rows))
    return data, bounds


def compute_distance(pos1: complex, pos2: complex) -> complex:
    return complex(pos2.real - pos1.real, pos2.imag - pos1.imag)


def compute_antinode_position(pair: tuple[complex, complex]) -> complex:
    l, r = pair
    dist = compute_distance(l, r)
    new_position = r + dist
    return new_position


def compute_next_position(position: complex, distance: complex) -> complex:
    return position + distance


def get_antinode_positions(
    node_map: dict[str, set[complex]], bounds: Bounds
) -> set[complex]:
    antinode_positions: set[complex] = set()
    for k, v in node_map.items():
        for pair in permutations(v, 2):
            new_antinode_position = compute_antinode_position(pair)
            if bounds.in_bounds(new_antinode_position):
                antinode_positions.add(new_antinode_position)
    return antinode_positions


def get_resonant_antinode_positions(
    node_map: dict[str, set[complex]], bounds: Bounds
) -> set[complex]:
    antinode_positions: set[complex] = set()
    for k, v in node_map.items():
        for pair in permutations(v, 2):
            antinode_positions.update(pair)
            distance = compute_distance(*pair)
            current_position = pair[1]
            while True:
                current_position += distance
                if bounds.in_bounds(current_position):
                    antinode_positions.add(current_position)
                else:
                    break
    return antinode_positions


def part_a_example():
    pair1 = (complex(0, 0), complex(0, 1))
    antinode_position = compute_antinode_position(pair1)
    assert antinode_position == complex(0, 2)

    pair2 = (complex(0, 1), complex(0, 0))
    antinode_position = compute_antinode_position(pair2)
    assert antinode_position == complex(0, -1)

    pair3 = (complex(0, 0), complex(2, 2))
    antinode_position = compute_antinode_position(pair3)
    assert antinode_position == complex(4, 4)

    fp = "./example/day08-example01.txt"
    node_map, bounds = parse_data(fp)
    antinode_positions = get_antinode_positions(node_map, bounds)
    print(len(antinode_positions), "= 2")

    fp = "./example/day08-example02.txt"
    node_map, bounds = parse_data(fp)
    antinode_positions = get_antinode_positions(node_map, bounds)
    print(len(antinode_positions), "= 14")


def part_a():
    fp = "./data/day08.txt"
    node_map, bounds = parse_data(fp)
    antinode_positions = get_antinode_positions(node_map, bounds)
    print(len(antinode_positions))


def part_b_example():
    fp = "./example/day08-example02.txt"
    node_map, bounds = parse_data(fp)
    antinode_positions = get_resonant_antinode_positions(node_map, bounds)
    print(len(antinode_positions), "= 34")

    fp = "./example/day08-example03.txt"
    node_map, bounds = parse_data(fp)
    antinode_positions = get_resonant_antinode_positions(node_map, bounds)
    print(len(antinode_positions), "= 9")


def part_b():
    fp = "./data/day08.txt"
    node_map, bounds = parse_data(fp)
    antinode_positions = get_resonant_antinode_positions(node_map, bounds)
    print(len(antinode_positions))


if __name__ == "__main__":
    # part_a_example()
    part_a()
    # part_b_example()
    part_b()
