import matplotlib.pyplot as plt
import matplotlib.cm as cm

EXAMPLE = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIKIIJJEE
MIIIKIJEEE
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
        borders = [(y,x,y+1,x,'L'), (y,x,y,x+1,'T'),(y+1,x,y+1,x+1,'B'),(y, x+1,y+1, x+1,'R')]
        for border in borders:
            # Create a border without the last index for comparison
            border_without_direction = border[:4]

            if border_without_direction in {b[:4] for b in perimeter}:
                # Remove the full border if it matches (ignoring direction)
                perimeter = {b for b in perimeter if b[:4] != border_without_direction}
            else:
                # Add the border to the set
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
    num_lines = len(lines)
    colormap = cm.get_cmap('viridis', num_lines)
    colors = [colormap(i) for i in range(num_lines)]
    if lines:
        for i, line in enumerate(lines):
            y1, x1, y2, x2, _ = line
            # Invert y-coordinates for proper positioning
            ax.plot([x1, x2], [-y1+1, -y2+1], color=colors[i], linewidth=6)

    # Set the grid limits and aspect ratio
    ax.set_xlim(min_x - 0.5, max_x + 1.5)
    ax.set_ylim(-max_y - 1.5, -min_y + 0.5)
    ax.set_aspect("equal")

    # Remove axes for clarity
    plt.axis("off")

    # Show the plot
    plt.show()

def merge_lines(lines_collection):
    merged_lines = [lines_collection[0]]

    for y1, x1, y2, x2, Q in lines_collection[1:]:
        prev_y1, prev_x1, prev_y2, prev_x2, prev_Q = merged_lines[-1]

        # If the previous line's end matches the current line's start, merge them
        if (prev_y2, prev_x2) == (y1, x1) and Q == prev_Q:
            merged_lines[-1] = (prev_y1, prev_x1, y2, x2, Q)
        else:
            # Otherwise, add the current line as a new segment
            merged_lines.append((y1, x1, y2, x2, Q))

    return merged_lines

def extract_facets(zone):
    vectors = calculate_perimeter(zone)
    lines_directions_x = sorted(
        (v for v in vectors if (v[2] - v[0], v[3] - v[1]) == (1, 0)),
        key=lambda v: (v[1], v[3], v[0], v[2], v[4])
    )
    lines_directions_y = sorted(
        (v for v in vectors if (v[2] - v[0], v[3] - v[1]) == (0, 1)),
        key=lambda v: (v[0], v[2], v[1], v[3], v[4])
    )
    #render_map(zone, merge_lines(lines_directions_x) + merge_lines(lines_directions_y))
    return len(merge_lines(lines_directions_x)) + len(merge_lines(lines_directions_y))


def part2():
    map = parse_input(open("input").read())
    zones = extract_zones(map)
    extract_facets(zones[0])
    #extract facets of each zone
    return sum(len(zone) * extract_facets(zone) for zone in zones)

print(f"Part 2 : {part2()}")