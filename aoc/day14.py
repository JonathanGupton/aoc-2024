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
    robot_locations = robots[:, :1]
    top_left = robots[(robots[:, 0] <= q_width) & (robots[:, 1] <= q_height)]
    top_right = robots[
        (width - q_width < robots[:, 0])
        & (robots[:, 0] <= width)
        & (robots[:, 1] <= q_height)
    ]
    bottom_left = robots[
        (robots[:, 0] <= q_width)
        & (height - q_height < robots[:, 1])
        & (robots[:, 1] <= height)
    ]
    bottom_right = robots[
        (width - q_width < robots[:, 0])
        & (robots[:, 0] <= width)
        & (height - q_height < robots[:, 1])
        & (robots[:, 1] <= height)
    ]
    return top_left, top_right, bottom_left, bottom_right


def example_a():
    fp = "./example/day14-example02.txt"
    robots = parse_data(fp)
    dimensions = (11, 7)
    robots = advance_robots(robots, dimensions)
    robots = advance_robots(robots, dimensions)
    robots = advance_robots(robots, dimensions)
    robots = advance_robots(robots, dimensions)
    robots = advance_robots(robots, dimensions)  # 11, 7
    robots = advance_robots(robots, dimensions)


if __name__ == "__main__":
    fp = "./example/day14-example01.txt"
    robots = parse_data(fp)
    dimensions = (11, 7)  # 11 wide, 7 tall
    for _ in range(100):
        robots = advance_robots(robots, dimensions)
    t_l, t_r, b_l, b_r = compute_quadrant_census(robots, dimensions)
