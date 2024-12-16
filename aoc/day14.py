from collections import defaultdict
import re
import numpy as np


def parse_data(fp: str) -> np.ndarray:
    output = []
    pattern = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"
    with open(fp, "r") as f:
        for line in f.readlines():
            match = re.match(pattern, line)
            p_x, p_y, v_x, v_y = map(int, match.groups())
            output.append((p_x, p_y, v_x, v_y))
    arr = np.array(output)
    return arr


def create_robot_str(configuration: np.ndarray, dims: tuple[int, int]) -> str:
    width, height = dims
    field = [["." for x in range(width)] for _ in range(height)]
    positions = defaultdict(int)
    for x, y in configuration[:, :2]:
        positions[(x, y)] += 1
    for (x, y), v in positions.items():
        field[y][x] = str(v)
    output_str = "\n".join(["".join(line) for line in field])
    return output_str


def print_robots(configuration: np.ndarray, dims: tuple[int, int]) -> None:
    output_str = create_robot_str(configuration, dims)
    print(output_str, sep="\r" * len(output_str))


def advance_robots(robots: np.ndarray, dims: tuple[int, int]) -> np.ndarray:
    width, height = dims
    robots[:, 0] += robots[:, 2]
    robots[:, 1] += robots[:, 3]
    robots[robots[:, 0] < 0, 0] += width
    robots[robots[:, 0] >= width, 0] -= width
    robots[robots[:, 1] < 0, 1] += height
    robots[robots[:, 1] >= height, 1] -= height
    return robots


def compute_quadrant_census(
    robots: np.ndarray, dims: tuple[int, int]
) -> tuple[int, int, int, int]:
    width, height = dims
    q_width, q_height = width // 2, height // 2
    top_half = robots[:, 1] < q_height
    bottom_half = robots[:, 1] > q_height
    left_half = robots[:, 0] < q_width
    right_half = robots[:, 0] > q_width
    top_left = robots[top_half & left_half]
    top_right = robots[top_half & right_half]
    bottom_left = robots[bottom_half & left_half]
    bottom_right = robots[bottom_half & right_half]
    return len(top_left), len(top_right), len(bottom_left), len(bottom_right)


def example_a():
    fp = "./example/day14-example02.txt"
    robots = parse_data(fp)
    dimensions = (11, 7)
    print_robots(robots, dimensions)
    for i in range(5):
        robots = advance_robots(robots, dimensions)
        print(i + 1)
        print_robots(robots, dimensions)

    fp = "./example/day14-example01.txt"
    robots = parse_data(fp)
    dimensions = (11, 7)  # 11 wide, 7 tall
    for _ in range(100):
        robots = advance_robots(robots, dimensions)
    t_l, t_r, b_l, b_r = compute_quadrant_census(robots, dimensions)
    safety_factor = t_l * t_r * b_l * b_r
    print(safety_factor)


def part_a():
    fp = "./data/day14.txt"
    robots = parse_data(fp)
    width = 101
    height = 103
    dimensions = (width, height)
    for _ in range(100):
        robots = advance_robots(robots, dimensions)
    t_l, t_r, b_l, b_r = compute_quadrant_census(robots, dimensions)
    safety_factor = t_l * t_r * b_l * b_r
    print(safety_factor)


def part_b():
    fp = "./data/day14.txt"
    robots = parse_data(fp)
    width = 101
    height = 103
    dimensions = (width, height)
    iterations = 0
    output_file = "./output/robot_positions.txt"
    with open(output_file, "a") as f:
        for i in range(7000):
            iterations += 1
            robots = advance_robots(robots, dimensions)
            print(iterations, sep="\n")
            robot_str = create_robot_str(robots, dimensions)
            f.write(f"Iteration {iterations}:\n{robot_str}\n\n")


if __name__ == "__main__":
    example_a()
    part_a()
    part_b()
