from collections import deque
from itertools import product
from typing import Generator
from typing import Sequence

DIRECTIONS = (complex(1, 0), complex(0, 1), complex(-1, 0), complex(0, -1))
HORIZONTAL_DIRECTIONS = [complex(1, 0), complex(-1, 0)]
VERTICAL_DIRECTIONS = [complex(0, -1), complex(0, 1)]
DIRECTIONS_PERPENDICULAR = {
    HORIZONTAL_DIRECTIONS[0]: VERTICAL_DIRECTIONS,
    HORIZONTAL_DIRECTIONS[1]: VERTICAL_DIRECTIONS,
    VERTICAL_DIRECTIONS[0]: HORIZONTAL_DIRECTIONS,
    VERTICAL_DIRECTIONS[1]: HORIZONTAL_DIRECTIONS,
}


def parse_data(fp: str) -> tuple[dict[complex, str], tuple[int, int]]:
    output = {}
    with open(fp, "r") as f:
        for y, row in enumerate(f.readlines()):
            for x, val in enumerate(row.strip()):
                output[complex(x, y)] = val
    bounds = (x + 1, y + 1)
    return output, bounds


def next_directions(
    start: complex, directions: tuple[complex, ...] = DIRECTIONS
) -> Generator[complex, None, None]:
    for direction in directions:
        yield start + direction


def find_adjacent_plots(
    start: complex, garden_plots: dict[complex, str]
) -> set[complex]:
    seen: set[complex] = set()
    adjacent: set[complex] = set()
    q = deque([start])
    plot_type = garden_plots[start]
    seen.add(start)
    adjacent.add(start)
    while q:
        current = q.popleft()
        seen.add(current)
        for direction in next_directions(current):
            if direction not in seen and garden_plots.get(direction) == plot_type:
                adjacent.add(direction)
                q.appendleft(direction)
    return adjacent


def get_plot_areas(
    garden_plots: dict[complex, str], bounds: tuple[int, int]
) -> deque[set[complex]]:
    seen = set()
    plot_collections = deque()
    x_max, y_max = bounds
    for x, y in product(range(x_max), range(y_max)):
        if complex(x, y) in seen:
            continue
        else:
            plots = find_adjacent_plots(complex(x, y), garden_plots)
            plot_collections.append(plots)
            seen.update(plots)
    return plot_collections


def compute_plot_perimeter(plot: set[complex]) -> int:
    perimeter = 0
    for single_plot in plot:
        for direction in next_directions(single_plot):
            if direction not in plot:
                perimeter += 1
    return perimeter


def get_full_plot_perimeters(plot_areas: Sequence[set[complex]]) -> list[int]:
    perimeters = []
    for area in plot_areas:
        perimeters.append(compute_plot_perimeter(area))
    return perimeters


def traverse_fence_edge(
    start: complex, area: set[complex], perpendicular_direction: complex
) -> frozenset[tuple[complex, complex]]:
    seen = set()
    for parallel in DIRECTIONS_PERPENDICULAR[perpendicular_direction]:
        q = deque()
        q.append(start)
        while q:
            current = q.popleft()
            seen.add((current, current + perpendicular_direction))
            if (
                current + parallel in area
                and (current + parallel + perpendicular_direction) not in area
            ):
                current = current + parallel
                q.append(current)
    return frozenset(seen)


def count_continuous_plot_edges(area: set[complex]) -> int:
    """Part B to find continuous perimeters"""
    edges: set[frozenset[tuple[complex, complex]]] = set()
    for plot in area:
        for direction in DIRECTIONS:
            if plot + direction not in area:  # it's an edge
                edges.add(traverse_fence_edge(plot, area, direction))
    return len(edges)


def get_continuous_plot_perimeters(plot_areas: Sequence[set[complex]]) -> list[int]:
    perimeters = []
    for area in plot_areas:
        perimeters.append(count_continuous_plot_edges(area))
    return perimeters


def calculate_fence_price(
    garden_plots: dict[complex, str], bounds: tuple[int, int]
) -> int:
    adjacent_plots = get_plot_areas(garden_plots, bounds)
    perimeters = get_full_plot_perimeters(adjacent_plots)
    total = 0
    for adjacent_plot, perimeter in zip(adjacent_plots, perimeters):
        total += len(adjacent_plot) * perimeter
    return total


def calculate_bulk_fence_price(
    garden_plots: dict[complex, str], bounds: tuple[int, int]
) -> int:
    adjacent_plots = get_plot_areas(garden_plots, bounds)
    perimeters = get_continuous_plot_perimeters(adjacent_plots)
    total = 0
    for adjacent_plot, perimeter in zip(adjacent_plots, perimeters):
        total += len(adjacent_plot) * perimeter
    return total


def part_a_examples():
    fp = r"./example/day12-example01.txt"
    data, bounds = parse_data(fp)
    fence_price = calculate_fence_price(data, bounds)
    print(fence_price, "= 140")

    fp = r"./example/day12-example02.txt"
    data, bounds = parse_data(fp)
    fence_price = calculate_fence_price(data, bounds)
    print(fence_price, "= 772")

    fp = r"./example/day12-example03.txt"
    data, bounds = parse_data(fp)
    fence_price = calculate_fence_price(data, bounds)
    print(fence_price, "= 1930")


def part_a():
    fp = r"./data/day12.txt"
    data, bounds = parse_data(fp)
    fence_price = calculate_fence_price(data, bounds)
    print(fence_price)


def part_b_examples():
    fp = r"./example/day12-example01.txt"
    data, bounds = parse_data(fp)
    fence_price = calculate_bulk_fence_price(data, bounds)
    print(fence_price, "= 80")

    fp = r"./example/day12-example02.txt"
    data, bounds = parse_data(fp)
    fence_price = calculate_bulk_fence_price(data, bounds)
    print(fence_price, "= 436")

    fp = r"./example/day12-example04.txt"
    data, bounds = parse_data(fp)
    fence_price = calculate_bulk_fence_price(data, bounds)
    print(fence_price, "= 236")

    fp = r"./example/day12-example05.txt"
    data, bounds = parse_data(fp)
    fence_price = calculate_bulk_fence_price(data, bounds)
    print(fence_price, "= 368")

    fp = r"./example/day12-example03.txt"
    data, bounds = parse_data(fp)
    fence_price = calculate_bulk_fence_price(data, bounds)
    print(fence_price, "= 1206")


def part_b():
    fp = r"./data/day12.txt"
    data, bounds = parse_data(fp)
    fence_price = calculate_bulk_fence_price(data, bounds)
    print(fence_price)


if __name__ == "__main__":
    part_a_examples()
    part_a()
    part_b_examples()
    part_b()
