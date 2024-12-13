from dataclasses import dataclass
import heapq
import re
import time


@dataclass
class Direction:
    x: int
    y: int
    cost: int = 0


@dataclass(unsafe_hash=True, order=True)
class Position:
    x: int
    y: int


@dataclass
class ClawMachine:
    A: Direction
    B: Direction
    Prize: Position


def parse_data(fp: str) -> list[ClawMachine]:
    claw_machines = []
    button_pattern = r"Button [AB]: X\+(\d+), Y\+(\d+)"
    prize_pattern = r"Prize: X=(\d+), Y=(\d+)"
    with open(fp, "r") as f:
        for chunk in f.read().split("\n\n"):
            button_a, button_b, prize = chunk.split("\n")

            button_a_match = re.match(button_pattern, button_a)
            direction_a = Direction(*map(int, button_a_match.groups()), cost=3)

            button_b_match = re.match(button_pattern, button_b)
            direction_b = Direction(*map(int, button_b_match.groups()), cost=1)

            prize_match = re.match(prize_pattern, prize)
            prize_location = Position(*map(int, prize_match.groups()))

            claw_machines.append(ClawMachine(direction_a, direction_b, prize_location))

    return claw_machines


def solve_machine(machine: ClawMachine, offset: int = 0) -> int:
    prize = Position(machine.Prize.x + offset, machine.Prize.y + offset)
    det = machine.A.x * machine.B.y - machine.A.y * machine.B.x
    a = int((prize.x * machine.B.y - prize.y * machine.B.x) / det)
    b = int((machine.A.x * prize.y - prize.x * machine.A.y) / det)
    if (machine.A.x * a + machine.B.x * b, machine.A.y * a + machine.B.y * b) == (
        prize.x,
        prize.y,
    ):
        return int(a * 3 + b)
    else:
        return 0


def example_a():
    fp = "./example/day13-example01.txt"
    data = parse_data(fp)
    cost = solve_machine(data[0])
    print(cost, "= 280")

    cost = solve_machine(data[1])
    print(cost, "= 0")

    cost = solve_machine(data[2])
    print(cost, "= 200")

    cost = solve_machine(data[3])
    print(cost, "= 0")


def part_a():
    fp = "./data/day13.txt"
    data = parse_data(fp)
    total = 0
    for machine in data:
        total += solve_machine(machine)
    print(total)


def part_b():
    fp = "./data/day13.txt"
    data = parse_data(fp)
    total = 0
    offset = 10000000000000
    for machine in data:
        total += solve_machine(machine, offset=offset)
    print(total)


if __name__ == "__main__":
    example_a()
    part_a()
    part_b()
