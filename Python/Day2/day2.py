puzzle = []

with open('input', 'r') as file:
    for line in file:
        values = line.split()
        puzzle.append([int(value) for value in values])

def is_increasing(level, max_gap):
    return all(0 < level[i+1] - level[i] <= max_gap for i in range(len(level)-1))

def is_decreasing(level, max_gap):
    return all(0 < level[i] - level[i+1] <= max_gap for i in range(len(level)-1))

def part1():
    result = sum(l==True for l in [is_increasing(level, 3) or is_decreasing(level,3) for level in puzzle])
    print(f"Result is {result}")

def is_increasing_tolerate(level, max_gap):
    return sum(is_increasing(level[:i] + level[i+1:], max_gap) for i in range(len(level))) > 0

def is_decreasing_tolerate(level, max_gap):
    return sum(is_decreasing(level[:i] + level[i + 1:], max_gap) for i in range(len(level))) > 0


def part2():
    result = sum(l==True for l in [is_increasing_tolerate(level, 3) or is_decreasing_tolerate(level,3) for level in puzzle])
    print(f"Result is {result}")

part1()
part2()
