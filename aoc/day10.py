from collections import deque
from string import digits
from typing import Generator

Coordinate = tuple[int, int]  # i, j or row, col
TopoMap = list[list[int | str]]


def get_next_direction(
    coord: Coordinate,
    directions: tuple[Coordinate] = ((-1, 0), (0, 1), (1, 0), (0, -1)),
) -> Generator[Coordinate, None, None]:
    for direction in directions:
        yield coord[0] + direction[0], coord[1] + direction[1]


def is_in_bounds(coord: Coordinate, topomap: TopoMap) -> bool:
    return 0 <= coord[0] < len(topomap) and 0 <= coord[1] < len(topomap[0])


def is_uphill(current_coordinate: Coordinate, nc: Coordinate, topomap: TopoMap) -> bool:
    return (
        topomap[nc[0]][nc[1]]
        == topomap[current_coordinate[0]][current_coordinate[1]] + 1
    )


def parse_data(fp: str) -> TopoMap:
    out = []
    with open(fp, "r") as f:
        for row in f.readlines():
            out.append([int(i) if i in digits else i for i in row.strip()])
    return out


def find_trailheads(tm: TopoMap) -> Generator[Coordinate, None, None]:
    """Check the top row and sides of the topographic map for 0's."""
    for i, row in enumerate(tm):
        for j, col in enumerate(row):
            if col == 0:
                yield i, j


def find_count_of_reachable_peaks(trailhead: Coordinate, topomap: TopoMap) -> int:
    q = deque([trailhead])
    seen: set[Coordinate] = set()
    peaks_seen: set[Coordinate] = set()
    while q:
        current = q.popleft()
        seen.add(current)
        if topomap[current[0]][current[1]] == 9:
            peaks_seen.add(current)
            continue
        for next_direction in get_next_direction(current):
            if (
                next_direction not in seen
                and is_in_bounds(next_direction, topomap)
                and is_uphill(current, next_direction, topomap)
            ):
                q.appendleft(next_direction)
    return len(peaks_seen)


def find_count_of_distinct_paths_to_peaks(
    trailhead: Coordinate, topomap: TopoMap
) -> int:
    paths = set()
    paths_to_peaks = set()
    q: deque[tuple[tuple[Coordinate], ...]] = deque(((trailhead,),))
    while q:
        current_path = q.popleft()
        current_position = current_path[-1]
        paths.add(current_path)
        if topomap[current_position[0]][current_position[1]] == 9:
            paths_to_peaks.add(current_path)
            continue
        for next_position in get_next_direction(current_position):
            if (
                current_path + (next_position,) not in paths
                and is_in_bounds(next_position, topomap)
                and is_uphill(current_position, next_position, topomap)
            ):
                next_path = current_path + (next_position,)
                q.append(next_path)
    return len(paths_to_peaks)


def calculate_path_score(topomap: TopoMap) -> int:
    trailheads = tuple(find_trailheads(topomap))
    paths = []
    for trailhead in trailheads:
        paths.append(find_count_of_reachable_peaks(trailhead, topomap))
    return sum(paths)


def calculate_path_rating(topomap: TopoMap) -> int:
    trailheads = tuple(find_trailheads(topomap))
    trail_counts = []
    for trailhead in trailheads:
        trail_counts.append(find_count_of_distinct_paths_to_peaks(trailhead, topomap))
    return sum(trail_counts)


def example_a():
    fp = "./example/day10-example01.txt"
    topomap = parse_data(fp)
    score = calculate_path_score(topomap)
    print(score, "= 1")

    fp = "./example/day10-example02.txt"
    topomap = parse_data(fp)
    score = calculate_path_score(topomap)
    print(score, "= 2")

    fp = "./example/day10-example03.txt"
    topomap = parse_data(fp)
    score = calculate_path_score(topomap)
    print(score, "= 4")

    fp = "./example/day10-example04.txt"
    topomap = parse_data(fp)
    score = calculate_path_score(topomap)
    print(score, "= 3")

    fp = "./example/day10-example05.txt"
    topomap = parse_data(fp)
    score = calculate_path_score(topomap)
    print(score, "= 36")


def part_a():
    fp = "./data/day10.txt"
    topomap = parse_data(fp)
    score = calculate_path_score(topomap)
    print(score)


def example_b():
    fp = "./example/day10-example06.txt"
    topomap = parse_data(fp)
    score = calculate_path_rating(topomap)
    print(score, "= 3")

    fp = "./example/day10-example07.txt"
    topomap = parse_data(fp)
    score = calculate_path_rating(topomap)
    print(score, "= 13")

    fp = "./example/day10-example08.txt"
    topomap = parse_data(fp)
    score = calculate_path_rating(topomap)
    print(score, "= 227")

    fp = "./example/day10-example05.txt"
    topomap = parse_data(fp)
    score = calculate_path_rating(topomap)
    print(score, "= 81")


def part_b():
    fp = "./data/day10.txt"
    topomap = parse_data(fp)
    score = calculate_path_rating(topomap)
    print(score)


if __name__ == "__main__":
    example_a()
    part_a()
    example_b()
    part_b()
