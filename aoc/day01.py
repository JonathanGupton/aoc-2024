from collections import Counter
from pathlib import Path
import re


def get_data(filepath: Path) -> str:
    with open(filepath, "r") as f:
        data = f.read()
    return data


def parse_data(data: str) -> tuple[list[int], list[int]]:
    l_vals, r_vals = [], []
    for row in data.strip().split("\n"):
        matches = re.match(r"(\d*)\s+(\d*)", row)
        l_vals.append(int(matches.group(1)))
        r_vals.append(int(matches.group(2)))
    l_vals.sort()
    r_vals.sort()
    return l_vals, r_vals


def difference_of_two_lists(list_a: list[int], list_b: list[int]) -> int:
    dist = 0
    for x, y in zip(list_a, list_b):
        dist += abs(x - y)
    return dist


def calculate_similarity(list_a: list[int], weights: dict[int, int]) -> int:
    similarity = 0
    for n in list_a:
        similarity += n * weights.get(n, 0)
    return similarity


def part_one():
    fp = "data/day01.txt"
    data_src = Path(fp)
    data = get_data(data_src)
    l_vals, r_vals = parse_data(data)
    dist = difference_of_two_lists(l_vals, r_vals)
    print(dist)


def part_two():
    fp = "data/day01.txt"
    data_src = Path(fp)
    data = get_data(data_src)
    l_vals, r_vals = parse_data(data)
    r_counts = Counter(r_vals)
    similarity = calculate_similarity(l_vals, r_counts)
    print(similarity)


if __name__ == '__main__':
    part_one()
    part_two()
