from collections import defaultdict
from collections import deque
from pathlib import Path


def get_data(filepath: Path) -> str:
    with open(filepath, "r") as f:
        data = f.read()
    return data


def parse_data(
    input_val: str,
) -> tuple[dict[int, set[int]], tuple[tuple[int, ...], ...]]:
    rules, updates = input_val.strip().split("\n\n")
    ordering_rules = defaultdict(set)
    for rule in rules.split("\n"):
        before, after = map(int, rule.split("|"))
        ordering_rules[before].add(after)
    update_vals = tuple(
        tuple(map(int, nums.split(","))) for nums in updates.split("\n")
    )
    return ordering_rules, update_vals


def reverse_order_dict(orders: dict[int, set[int]]) -> dict[int, set[int]]:
    reverse = defaultdict(set)
    for k, v in orders.items():
        for n in v:
            reverse[n].add(k)
    return reverse


def is_correctly_ordered(
    update: tuple[int, ...], order_rules: dict[int, set[int]]
) -> bool:
    update_set = set(update)
    for n in update[::-1]:
        update_set.remove(n)
        if not update_set.issubset(order_rules[n]):
            return False
    return True


def get_middle_page_number(rule: tuple[int, ...]) -> int:
    return rule[len(rule) // 2]


def re_order_pages(
    rule: tuple[int, ...], orders: dict[int, set[int]]
) -> tuple[int, ...]:
    rule_set: set[int] = set(rule)
    rule_q: deque[int] = deque(rule)
    reordered: deque[int] = deque()
    while rule_q:
        r = rule_q.popleft()
        rule_set.remove(r)
        if rule_set.issubset(orders[r]):
            reordered.append(r)
            continue
        else:
            rule_set.add(r)
            rule_q.append(r)
    return tuple(reordered)


def part_a_example_1():
    fp = Path("./example/day05-example-01.txt")
    data = get_data(fp)
    orders, updates = parse_data(data)
    reverse_orders = reverse_order_dict(orders)
    result = 0
    for rule in updates:
        if is_correctly_ordered(rule, reverse_orders):
            result += get_middle_page_number(rule)
    print(result, "= 143")


def part_a():
    fp = Path("./data/day05.txt")
    data = get_data(fp)
    orders, updates = parse_data(data)
    reverse_orders = reverse_order_dict(orders)
    result = 0
    for rule in updates:
        if is_correctly_ordered(rule, reverse_orders):
            result += get_middle_page_number(rule)
    print(result)


def part_b_example_1():
    fp = Path("./example/day05-example-01.txt")
    data = get_data(fp)
    orders, updates = parse_data(data)
    reverse_orders = reverse_order_dict(orders)

    result = 0
    for rule in updates:
        if not is_correctly_ordered(rule, reverse_orders):
            new_rule = re_order_pages(rule, orders)
            result += get_middle_page_number(new_rule)
    print(result, " = 123")


def part_b():
    fp = Path("./data/day05.txt")
    data = get_data(fp)
    orders, updates = parse_data(data)
    reverse_orders = reverse_order_dict(orders)

    result = 0
    for rule in updates:
        if not is_correctly_ordered(rule, reverse_orders):
            new_rule = re_order_pages(rule, orders)
            result += get_middle_page_number(new_rule)
    print(result)


if __name__ == "__main__":
    part_a_example_1()
    part_a()
    part_b_example_1()
    part_b()
