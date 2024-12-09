from dataclasses import dataclass
from collections import deque
from more_itertools import chunked
from typing import Iterable


@dataclass
class Disk:
    idx: int
    files: int
    free: int = 0


def parse_data(fp: str) -> list[Disk]:
    disk_space = []
    with open(fp, "r") as f:
        for idx, vals in enumerate(chunked(f.read().strip(), 2)):
            disk_space.append(Disk(*map(int, (idx, *vals))))
    return disk_space


def checksum(files: Iterable[int | None]) -> int:
    checksum_value = 0
    for idx, val in enumerate(files):
        checksum_value += idx * val
    return checksum_value


def defragment_disk_blocks(disk_space=list[Disk]) -> deque[int]:
    output_queue = deque()
    disk_space = deque(disk_space)
    while disk_space:
        left_file = disk_space.popleft()
        for i in range(left_file.files):
            output_queue.append(left_file.idx)
        while disk_space and left_file.free:
            right_file = disk_space.pop()
            to_distribute = min(left_file.free, right_file.files)
            for _ in range(to_distribute):
                output_queue.append(right_file.idx)
            right_file.files -= to_distribute
            left_file.free -= to_distribute
            if right_file.files:
                disk_space.append(right_file)
    return output_queue


def defragment_disk_files(disk_space=list[Disk]):
    disks = deque(disk_space)
    hold = deque()
    to_check = len(disk_space)
    while to_check:
        append = False
        to_check -= 1
        disk = disks.pop()
        for i in range(len(disks)):
            if disk.files <= disks[i].free:
                append = True
                break
        if append:
            disks[-1].free += disk.free + disk.files
            disks[i].free, disk.free = 0, disks[i].free - disk.files
            disks.insert(i + 1, disk)
        else:
            hold.appendleft(disk)
    disks.extend(hold)
    return disks


def transform_disk_queue_to_blocks(disk_queue: deque[Disk]) -> list[int]:
    blocks = []
    for disk in disk_queue:
        for _ in range(disk.files):
            blocks.append(disk.idx)
        for _ in range(disk.free):
            blocks.append(0)
    return blocks


def example_a():
    fp = "./example/day09-example01.txt"
    data = parse_data(fp)
    q = deque(map(int, "0099811188827773336446555566"))
    defragmented = defragment_disk_blocks(data)
    try:
        assert q == defragmented
    except AssertionError:
        from itertools import zip_longest

        for idx, (l, r) in enumerate(zip_longest(q, defragmented)):
            print(idx, l, r)

    checksum_value = checksum(defragmented)
    assert checksum_value == 1928
    print(checksum_value, "= 1928")


def part_a():
    fp = "./data/day09.txt"
    disk_space = parse_data(fp)
    defrag_disk = defragment_disk_blocks(disk_space)
    cs = checksum(defrag_disk)
    print(cs)


def example_b():
    fp = "./example/day09-example01.txt"
    data = parse_data(fp)
    defragmented = defragment_disk_files(data)
    blocks = transform_disk_queue_to_blocks(defragmented)
    cs = checksum(blocks)
    print(cs, "= 2858")


def part_b():
    fp = "./data/day09.txt"
    disk_space = parse_data(fp)
    defragmented = defragment_disk_files(disk_space)
    blocks = transform_disk_queue_to_blocks(defragmented)
    cs = checksum(blocks)
    print(cs)


if __name__ == "__main__":
    example_a()
    part_a()
    example_b()
    part_b()
