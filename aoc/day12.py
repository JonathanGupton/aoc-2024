from collections import deque
from itertools import product
from typing import Sequence

DIRECTIONS = (complex(1, 0), complex(0, 1), complex(-1, 0), complex(0, -1))


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
) -> complex:
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


def compute_single_plot_perimeter(
    single_plot: complex, garden_plots: dict[complex, str]
) -> int:
    pass


def compute_plot_perimeter(plot: set[complex], garden_plots: dict[complex, str]) -> int:
    pass


def get_full_plot_perimeters(
    plot_areas: Sequence[set[complex]], garden_plots: dict[complex, str]
) -> list[int]:
    perimeters = []
    for area in plot_areas:
        perimeters.append(compute_plot_perimeter(area, garden_plots))
    return perimeters


if __name__ == "__main__":
    fp = r"./example/day12-example01.txt"
    data, bounds = parse_data(fp)
    adjacent_plots = get_plot_areas(data, bounds)
