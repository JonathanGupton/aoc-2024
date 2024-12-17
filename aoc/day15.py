from collections import deque


DIRECTION = {
    "<": complex(-1, 0),
    ">": complex(1, 0),
    "^": complex(0, -1),
    "v": complex(0, 1),
}


def draw_warehouse(
    warehouse_map: dict[complex, str], dimensions: tuple[int, int]
) -> str:
    warehouse_array = [
        ["." for _ in range(dimensions[0])] for _ in range(dimensions[1])
    ]
    for k, v in warehouse_map.items():
        x, y = int(k.real), int(k.imag)
        warehouse_array[y][x] = v
    warehouse_str = "\n".join("".join(row) for row in warehouse_array) + "\n"
    return warehouse_str


def parse_data(fp: str) -> tuple[dict[complex, str], str, tuple[int, int]]:
    warehouse_map = {}
    with open(fp, "r") as f:
        warehouse_map_str, directions = f.read().split("\n\n")
        for y, row in enumerate(warehouse_map_str.strip().splitlines()):
            for x, col in enumerate(row):
                if col != ".":
                    warehouse_map[complex(x, y)] = col

        directions = "".join(d for d in directions.strip().splitlines())
    dimensions = (x + 1, y + 1)
    return warehouse_map, directions, dimensions


def get_robot_position(warehouse_map: dict[complex, str]) -> complex:
    for k, v in warehouse_map.items():
        if v == "@":
            return k


def get_single_gps_coordinate_score(object_location: complex) -> int:
    return int(object_location.real + object_location.imag * 100)


def compute_total_gps_score(warehouse_map: dict[complex, str]) -> int:
    total = 0
    for coordinate, v in warehouse_map.items():
        if v == "O":
            total += get_single_gps_coordinate_score(coordinate)
    return total


def move_is_unobstructed(
    object_location: complex, direction: str, warehouse_map: dict[complex, str]
) -> bool:
    current_location = object_location
    while True:
        next_location = current_location + DIRECTION[direction]
        next_location_object = warehouse_map.get(next_location)
        if next_location_object is None:
            return True
        if next_location_object == "#":
            return False
        if next_location_object == "O":
            current_location = next_location


def move_robot(warehouse_map: dict[complex, str], direction: str) -> dict[complex, str]:
    direction_vector = DIRECTION[direction]
    current = get_robot_position(warehouse_map)
    stack = deque([current])
    while True:
        if warehouse_map.get(current + direction_vector) is None:
            while stack:
                last = stack.pop()
                warehouse_map[last + direction_vector] = warehouse_map.get(last)
            del warehouse_map[last]
            break
        if warehouse_map.get(current + direction_vector) == "#":
            break
        if warehouse_map.get(current + direction_vector) == "O":
            current = current + direction_vector
            stack.append(current)
    return warehouse_map


def example_a():
    fp = r"./example/day15-example01.txt"
    warehouse_map, directions, dimensions = parse_data(fp)
    for i, direction in enumerate(directions):
        # print(draw_warehouse(warehouse_map, dimensions))
        warehouse_map = move_robot(warehouse_map, direction)

    # print(draw_warehouse(warehouse_map, dimensions))
    total = compute_total_gps_score(warehouse_map)
    print(total, "= 2028")

    fp = r"./example/day15-example02.txt"
    warehouse_map, directions, dimensions = parse_data(fp)
    for i, direction in enumerate(directions):
        # print(draw_warehouse(warehouse_map, dimensions))
        warehouse_map = move_robot(warehouse_map, direction)

    # print(draw_warehouse(warehouse_map, dimensions))
    total = compute_total_gps_score(warehouse_map)
    print(total, "= 10092")


def part_a():
    fp = r"./data/day15.txt"
    warehouse_map, directions, dimensions = parse_data(fp)
    for i, direction in enumerate(directions):
        # print(draw_warehouse(warehouse_map, dimensions))
        warehouse_map = move_robot(warehouse_map, direction)

    # print(draw_warehouse(warehouse_map, dimensions))
    total = compute_total_gps_score(warehouse_map)
    print(total)


if __name__ == "__main__":
    example_a()
    part_a()
