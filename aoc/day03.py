from pathlib import Path
import re


def get_data(filepath: Path) -> str:
    with open(filepath, "r") as f:
        data = f.read()
    return data


def multiply(ops: str) -> int:
    num_pattern = r"mul\((\d*),(\d*)\)"
    results = re.match(num_pattern, ops)
    return int(results.group(1)) * int(results.group(2))


def parse_and_process_mul(instructions: str) -> int:
    mul_pattern = r"mul\(\d*,\d*\)"
    total = 0
    for val in re.findall(mul_pattern, instructions):
        total += multiply(val)
    return total


def parse_and_process_with_dos_and_donts(instructions: str) -> int:
    do_check_pattern = r"(mul\(\d*,\d*\))|(do\(\))|(don't\(\))"
    total = 0
    dont_flag = False
    for val in re.findall(do_check_pattern, instructions):
        match val:
            case ("", "do()", ""):
                if dont_flag:
                    dont_flag = False
            case ("", "", "don't()"):
                dont_flag = True
            case (ops, "", ""):
                if dont_flag:
                    continue
                total += multiply(ops)
    return total


def part_a_example():
    example1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    result = parse_and_process_mul(example1)
    print(result)  # 161


def part_a():
    fp = Path(r"data/day03.txt")
    instructions = get_data(fp)
    result = parse_and_process_mul(instructions)
    print(result)


def part_b_example():
    example2 = (
        r"xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
    result = parse_and_process_with_dos_and_donts(example2)
    print(result)  # 48


def part_b():
    fp = Path(r"data/day03.txt")
    instructions = get_data(fp)
    result = parse_and_process_with_dos_and_donts(instructions)
    print(result)


if __name__ == "__main__":
    part_a_example()
    part_a()
    part_b_example()
    part_b()
