from collections import deque


DIRECTION = {
    "<": complex(-1, 0),
    ">": complex(1, 0),
    "^": complex(0, -1),
    "V": complex(0, 1),
}


def parse_data(fp: str) -> tuple[dict[complex, str], str]:
    warehouse_map = {}
    with open(fp, "r") as f:
        warehouse_map_str, directions = f.read().split("\n\n")
        for y, row in enumerate(warehouse_map_str.strip().splitlines()):
            for x, col in enumerate(row):
                if col != ".":
                    warehouse_map[complex(x, y)] = col

        directions = "".join(d for d in directions.strip().splitlines())
    return warehouse_map, directions


def get_robot_position(warehouse_map: dict[complex, str]) -> complex:
    for k, v in warehouse_map.items():
        if v == "@":
            return k


def get_gps_coordinate(object_location: complex) -> int:
    return int(object_location.real * 100 + object_location.imag)


def compute_total_gps_score(warehouse_map: dict[complex, str]) -> int:
    total = 0
    for k, v in warehouse_map:
        if v == "O":
            total += get_gps_coordinate(k)


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
    robot_location = get_robot_position(warehouse_map)
    current_location = robot_location
    stack = deque()
    if move_is_unobstructed(current_location, direction, warehouse_map):
        while True:
            stack.append(current_location)
            next_location = current_location + DIRECTION[direction]
            next_location_object = warehouse_map.get(next_location)
            if next_location_object is None:
                while stack:
                    end = stack.pop()
                    warehouse_map[end + DIRECTION[direction]] = warehouse_map[end]
                del warehouse_map[robot_location]
            else:
                current_location = next_location
    return warehouse_map


if __name__ == "__main__":
    fp = r"./example/day15-example01.txt"
    warehouse_map, directions = parse_data(fp)
    for direction in directions:
        warehouse_map = move_robot(warehouse_map, direction)
    total = compute_total_gps_score(warehouse_map)
    print(total)
