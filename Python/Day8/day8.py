from itertools import combinations

EXAMPLE_DATA = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

def parse_input(data):
    lines = data.strip().split('\n')
    return {
        char: [(y, x) for y, line in enumerate(lines)
                      for x, c in enumerate(line) if c == char]
        for char in set(''.join(lines)) if char != '.'
    }, len(lines), len(lines[0])

def get_vector(p1, p2):
    return p1[0] - p2[0], p1[1] - p2[1]

def is_within_map(point, map_width, map_height):
    x, y = point
    return 0 <= x < map_width and 0 <= y < map_height

def part1(file_data: str):
    """
    >>> part1(EXAMPLE_DATA)
    14
    """
    antennas, height, width = parse_input(file_data)
    antinodes = set()
    for _, positions in antennas.items():
        for p1, p2 in combinations(positions, 2):
            antinode_p1 = (p1[0] + get_vector(p1, p2)[0], p1[1] + get_vector(p1, p2)[1])
            antinode_p2 = (p2[0] + get_vector(p2, p1)[0], p2[1] + get_vector(p2, p1)[1])
            if is_within_map(antinode_p1, width, height):
                antinodes.add(antinode_p1)
            if is_within_map(antinode_p2, width, height):
                antinodes.add(antinode_p2)
    return len(antinodes)

def apply_vector(point, vector):
    return point[0] + vector[0], point[1] + vector[1]

def print_map(coordinates, width, height):
    grid = [['.' for _ in range(width)] for _ in range(height)]
    for y, x in coordinates:
        grid[y][x] = '#'
    for row in grid:
        print(''.join(row))

def part2(file_data: str):
    """
    >>> part2(EXAMPLE_DATA)
    34
    """
    antennas, height, width = parse_input(file_data)
    antinodes = set()
    for _, positions in antennas.items():
        for p1, p2 in combinations(positions, 2):
            current_antenna = apply_vector(p1, get_vector(p1, p2))
            while is_within_map(current_antenna, width, height):
                antinodes.add(current_antenna)
                current_antenna = apply_vector(current_antenna, get_vector(p1, p2))
            current_antenna = apply_vector(p2, get_vector(p2, p1))
            while is_within_map(current_antenna, width, height):
                antinodes.add(current_antenna)
                current_antenna = apply_vector(current_antenna, get_vector(p2, p1))
    # print(antinodes)
    print_map(antinodes, width, height)
    return len(antinodes)

print(f"Part1: {part1(open('input').read())}")
print(f"Part2: {part2(EXAMPLE_DATA)}")