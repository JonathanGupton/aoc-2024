from dataclasses import dataclass
from itertools import cycle
from itertools import product
from pathlib import Path

Position = tuple[str, complex]

ROTATIONS = (
    "^",
    ">",
    "V",
    "<",
)

MOVEMENT = {
    ">": complex(1, 0),
    "V": complex(0, 1),
    "<": complex(-1, 0),
    "^": complex(0, -1),
}


@dataclass
class Edge:
    x_min: int
    y_min: int
    x_max: int
    y_max: int

    def in_bounds(self, coordinate: complex):
        return (self.x_min <= coordinate.real < self.x_max) and (
            self.y_min <= coordinate.imag < self.y_max
        )


def get_data(filepath: Path) -> str:
    with open(filepath, "r") as f:
        data = f.read()
    return data


def parse_data(input_value: str) -> tuple[Position, dict[complex, str], Edge]:
    floorplan: dict[complex, str] = {}
    start: Position | None = None
    x = 0
    y = 0
    for y, line in enumerate(input_value.strip().split()):
        for x, c in enumerate(line):
            if c == "#":
                floorplan[complex(x, y)] = c
            elif c == "^":
                start = (c, complex(x, y))
    edges = Edge(0, 0, x + 1, y + 1)
    return start, floorplan, edges


def find_all_traversed_location_count(
    start: Position, floorplan: dict[complex, str], edges: Edge
) -> int:
    locations_seen: set[complex] = set()
    current_position: Position = start
    direction_cycler = cycle(ROTATIONS)
    direction = next(direction_cycler)
    while edges.in_bounds(current_position[1]):
        current_direction, current_coordinate = current_position
        locations_seen.add(current_coordinate)
        if floorplan.get(current_coordinate + MOVEMENT[direction]) == "#":
            direction = next(direction_cycler)
        else:
            current_coordinate += MOVEMENT[direction]
        current_position = (direction, current_coordinate)
    return len(locations_seen)


def path_has_a_loop(
    start: Position, floorplan: dict[complex, str], edges: Edge
) -> bool:
    direction_and_locations_seen: set[Position] = set()
    locations_seen: set[complex] = set()
    current_position: Position = start
    direction_cycler = cycle(ROTATIONS)
    direction = next(direction_cycler)
    while True:
        if current_position in direction_and_locations_seen:
            return True
        if not edges.in_bounds(current_position[1]):
            return False
        current_direction, current_coordinate = current_position
        direction_and_locations_seen.add(current_position)
        locations_seen.add(current_coordinate)
        if floorplan.get(current_coordinate + MOVEMENT[direction]) == "#":
            direction = next(direction_cycler)
        else:
            current_coordinate += MOVEMENT[direction]
        current_position = (direction, current_coordinate)


def part_a_example():
    fp = Path("./example/day06-example-01.txt")
    data = get_data(fp)
    start, floorplan, edges = parse_data(data)
    print(find_all_traversed_location_count(start, floorplan, edges), "= 41")


def part_a():
    fp = Path("./data/day06.txt")
    data = get_data(fp)
    start, floorplan, edges = parse_data(data)
    print(find_all_traversed_location_count(start, floorplan, edges))


def part_b_example():
    fp = Path("./example/day06-example-01.txt")
    data = get_data(fp)
    start, floorplan, edges = parse_data(data)
    loop_positions = 0
    for x, y in product(range(edges.x_max), range(edges.y_max)):
        coordinate = complex(x, y)
        if coordinate == start[1] or coordinate in floorplan:
            continue
        new_floorplan = floorplan.copy()
        new_floorplan[coordinate] = "#"
        if path_has_a_loop(start, new_floorplan, edges):
            loop_positions += 1
    print(loop_positions)


def part_b():
    fp = Path("./data/day06.txt")
    data = get_data(fp)
    start, floorplan, edges = parse_data(data)
    loop_positions = 0
    for x, y in product(range(edges.x_max), range(edges.y_max)):
        coordinate = complex(x, y)
        if coordinate == start[1] or coordinate in floorplan:
            continue
        new_floorplan = floorplan.copy()
        new_floorplan[coordinate] = "#"
        if path_has_a_loop(start, new_floorplan, edges):
            loop_positions += 1
    print(loop_positions)


if __name__ == "__main__":
    # part_a_example()
    # part_a()
    part_b()
