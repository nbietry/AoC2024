import matplotlib.pyplot as plt

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
    return perimeter

def part1():
    map = parse_input(open("input").read())
    zones = extract_zones(map)
    return sum(len(zone) * len(calculate_perimeter(zone)) for zone in zones)


#print(f"Part 1 : {part1()}")
def render_map(cells, lines=None):
    # Determine bounds of the grid based on the cell coordinates
    min_x = min(cell[1] for cell in cells)
    max_x = max(cell[1] for cell in cells)
    min_y = min(cell[0] for cell in cells)
    max_y = max(cell[0] for cell in cells)

    # Create a plot
    fig, ax = plt.subplots()

    # Draw cells (blue squares)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (y, x) in cells:
                # Filled cell
                ax.add_patch(plt.Rectangle((x, -y), 1, 1, color="blue"))
            else:
                # Empty cell (grid lines)
                ax.add_patch(plt.Rectangle((x, -y), 1, 1, edgecolor="black", fill=None))

    # Draw lines (red for borders)
    if lines:
        for line in lines:
            y1, x1, y2, x2 = line
            # Invert y-coordinates for proper positioning
            ax.plot([x1, x2], [-y1+1, -y2+1], color="red", linewidth=2)

    # Set the grid limits and aspect ratio
    ax.set_xlim(min_x - 0.5, max_x + 1.5)
    ax.set_ylim(-max_y - 1.5, -min_y + 0.5)
    ax.set_aspect("equal")

    # Remove axes for clarity
    plt.axis("off")

    # Show the plot
    plt.show()

def merge_lines(lines_collection):
    final_lines = []
    for line in lines_collection:
        y1, x1, y2, x2 = line
        if (y1,x1) in final_lines:
            final_lines.remove((y1,x1))
        final_lines.append((y2,x2))
    return final_lines

def extract_facets(zone):
    vectors = calculate_perimeter(zone)
    lines_directions_x = sorted(
        (v for v in vectors if (v[2] - v[0], v[3] - v[1]) == (1, 0)),
        key=lambda v: (v[1], v[3], v[0], v[2])
    )
    lines_directions_y = sorted(
        (v for v in vectors if (v[2] - v[0], v[3] - v[1]) == (0, 1)),
        key=lambda v: (v[0], v[2], v[1], v[3])
    )
    render_map(zone, lines_directions_x + lines_directions_y)
    return len(merge_lines(lines_directions_x)) + len(merge_lines(lines_directions_y))


def part2():
    map = parse_input(EXAMPLE)
    zones = extract_zones(map)
    extract_facets(zones[0])
    #extract facets of each zone
    return sum(len(zone) * extract_facets(zone) for zone in zones)

print(f"Part 2 : {part2()}")