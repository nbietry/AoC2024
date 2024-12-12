EXAMPLE = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

def parse_input(data:str):
    return [list(line) for line in data.splitlines()]

def depth_search(map, y, x):
    stack = [(y, x)]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    zone = {(y, x)}
    while stack:
        y, x = stack.pop()
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < len(map) and 0 <= nx < len(map[0]) and map[ny][nx] == map[y][x] and not (ny, nx) in zone:
                stack.append((ny, nx))
                zone.add((ny, nx))
    return zone

def extract_zones(map):
    map_height = len(map)
    map_width = len(map[0])
    map_visited = [[False for _ in range(map_width)] for _ in range(map_height)]
    zones = []
    for y in range(map_height):
        for x in range(map_width):
            if not map_visited[y][x]:
                current_zone = depth_search(map, y, x)
                zones.append(current_zone)
                #print(map[y][x], len(current_zone), current_zone)
                for cell in current_zone: map_visited[cell[0]][cell[1]] = True
    return zones

def calculate_perimeter(zone):
    perimeter = set()
    for y, x in zone:
        borders = [(y, x,y+1, x), (y,x,y,x+1),(y+1,x,y+1,x+1),(y, x+1,y+1, x+1)]
        for border in borders:
            if border  in perimeter:
                perimeter.remove(border)
            else:
                perimeter.add(border)
    return len(perimeter)

def part1():
    map = parse_input(open("input").read())
    zones = extract_zones(map)
    return sum(len(zone) * calculate_perimeter(zone) for zone in zones)


print(f"Part 1 : {part1()}")