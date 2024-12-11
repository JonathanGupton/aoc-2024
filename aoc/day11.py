from collections import deque
from functools import cache
from typing import Sequence


def parse_data(fp: str) -> list[int]:
    with open(fp, "r") as f:
        return [*map(int, f.read().strip().split())]


def get_evolved_stones_count(stones: Sequence[int], n_iterations: int) -> int:

    @cache
    def count_evolved_stones(stone: int, n_iterations: int) -> int:
        if n_iterations == 0:
            return 1
        else:
            total = 0
            if stone == 0:
                total += count_evolved_stones(1, n_iterations - 1)
            elif len(str(stone)) % 2 == 0:
                num_str = str(stone)
                new_num_lens = len(num_str) // 2
                total += count_evolved_stones(
                    int(num_str[new_num_lens:]), n_iterations - 1
                )
                total += count_evolved_stones(
                    int(num_str[:new_num_lens]), n_iterations - 1
                )
            else:
                total += count_evolved_stones(stone * 2024, n_iterations - 1)
            return total

    q = deque([(stone, n_iterations) for stone in stones])
    count = 0
    while q:
        next_val = q.popleft()
        count += count_evolved_stones(*next_val)
    return count


def example_a():
    fp = "./example/day11-example02.txt"
    data = parse_data(fp)
    count = get_evolved_stones_count(data, 2)
    print(count, "= 4")

    fp = "./example/day11-example02.txt"
    data = parse_data(fp)
    count = get_evolved_stones_count(data, 3)
    print(count, "= 5")

    fp = "./example/day11-example02.txt"
    data = parse_data(fp)
    count = get_evolved_stones_count(data, 25)
    print(count, "= 55312")


def part_a():
    fp = "./data/day11.txt"
    data = parse_data(fp)
    count = get_evolved_stones_count(data, 25)
    print(count)


def part_b():
    fp = "./data/day11.txt"
    data = parse_data(fp)
    count = get_evolved_stones_count(data, 75)
    print(count)


if __name__ == "__main__":
    example_a()
    part_a()
    part_b()
