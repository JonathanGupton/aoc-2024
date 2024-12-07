from typing import Sequence
from operator import add
from operator import mul


def parse_data(fp: str) -> list[tuple[int, tuple[int, ...]], ...]:
    out = []
    with open(fp, "r") as f:
        for line in f.readlines():
            result, nums = line.split(": ")
            result = int(result)
            nums = tuple(map(int, nums.split(" ")))
            out.append((result, nums))
    return out


def conc(x: int, y: int) -> int:
    """Concatenate two integers"""
    return int(str(x) + str(y))


def count_valid_operator_configurations(
    equations: list[tuple[int, tuple[int, ...]], ...]
) -> int:
    def _valid_configuration(
        target: int, lop: int, rops: Sequence[int], total: int = 0
    ) -> int:
        if target == lop and not rops:
            return 1
        if lop > target or not rops:
            return False
        for op in [add, mul]:
            new_lop = op(lop, rops[0])
            new_rops = tuple(rops[1:])
            total += _valid_configuration(target, new_lop, new_rops)
        return total

    total_valid_configurations = 0
    for eq in equations:
        target, nums = eq
        lops, nums = nums[0], tuple(nums[1:])
        if _valid_configuration(target, lops, nums):
            total_valid_configurations += target
        # total_valid_configurations += _valid_configuration(target, lops, nums)
    return total_valid_configurations


def count_valid_operator_configurations2(
    equations: list[tuple[int, tuple[int, ...]], ...]
) -> int:
    def _valid_configuration(
        target: int, lop: int, rops: Sequence[int], total: int = 0
    ) -> int:
        if target == lop and not rops:
            return 1
        if lop > target or not rops:
            return False
        for op in [add, mul, conc]:
            new_lop = op(lop, rops[0])
            new_rops = tuple(rops[1:])
            total += _valid_configuration(target, new_lop, new_rops)
        return total

    total_valid_configurations = 0
    for eq in equations:
        target, nums = eq
        lops, nums = nums[0], tuple(nums[1:])
        if _valid_configuration(target, lops, nums):
            total_valid_configurations += target
    return total_valid_configurations


def part_a_example1():
    fp = "./example/day07-example01.txt"
    data = parse_data(fp)
    print(count_valid_operator_configurations(data))


def part_a():
    fp = "./data/day07.txt"
    data = parse_data(fp)
    print(count_valid_operator_configurations(data))


def part_b_example1():
    fp = "./example/day07-example01.txt"
    data = parse_data(fp)
    print(count_valid_operator_configurations2(data))


def part_b():
    fp = "./data/day07.txt"
    data = parse_data(fp)
    print(count_valid_operator_configurations2(data))


if __name__ == "__main__":
    part_a_example1()
    part_a()
    part_b_example1()
    part_b()
