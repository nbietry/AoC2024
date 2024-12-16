import numpy as np
from matplotlib import pyplot as plt, animation
import matplotlib.colors as mcolors

EXAMPLE = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

EXAMPLE2 = """##############
##......##..##
##..........##
##....[][]@.##
##....[]....##
##..........##
##############

<vv<<^^<<^^"""

def parse_input(data: str):
    warehouse, moves = data.split('\n\n')
    warehouse = [list(line) for line in warehouse.splitlines()]
    return warehouse, moves

def find_start(warehouse):
    return ((y, x) for y, line in enumerate(warehouse) for x, char in enumerate(line) if char == '@')

def extract_things(warehouse, thing):
    return [(y, x) for y, line in enumerate(warehouse) for x, char in enumerate(line) if char == thing]

def get_next_position(warehouse, current, direction):
    if direction == 'v':
        return (current[0] + 1, current[1])
    elif direction == '^':
        return (current[0] - 1, current[1])
    elif direction == '>':
        return (current[0], current[1] + 1)
    elif direction == '<':
        return (current[0], current[1] - 1)

def render_map(warehouse, ax=None, save_frames=False, frames=None):
    """
    Render the warehouse map as a grid using matplotlib.

    Parameters:
    - warehouse: 2D list representing the current state of the map
    - ax: Optional matplotlib axis to render on
    - save_frames: Whether to save frames for animation
    - frames: List to store frames if save_frames is True
    """
    # Create a color mapping
    color_map = {
        '#': (0.3, 0.3, 0.3),      # Walls (dark gray)
        'O': (0.8, 0.4, 0.4),       # Stones (reddish)
        '[': (0.3, 0.4, 0.4),       # Stones (reddish)
        ']': (0.3, 0.4, 0.4),       # Stones (reddish)
        '@': (0.2, 0.7, 0.2),       # Robot (green)
        '.': (1, 1, 1)              # Empty space (white)
    }

    # Convert warehouse to numpy array of RGB values
    grid = np.zeros((len(warehouse), len(warehouse[0]), 3), dtype=float)
    for y, row in enumerate(warehouse):
        for x, cell in enumerate(row):
            grid[y, x] = color_map.get(cell, (1, 1, 1))

    # Create axis if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))

    # Clear previous plot and show new grid
    ax.clear()
    ax.imshow(grid, interpolation='nearest')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('Warehouse Map')

    # Save frame if needed
    if save_frames and frames is not None:
        frames.append(ax.get_figure())

    plt.tight_layout()
    plt.draw()
    plt.pause(0.5)  # Pause to show each move

def animate_map(map, moves):
    """
    Create an animation of the robot's movement through the warehouse.

    Parameters:
    - map: Initial warehouse map
    - moves: String of movement directions
    """
    # Prepare for animation
    fig, ax = plt.subplots(figsize=(10, 10))
    frames = []

    # Initial render
    render_map(map, ax, save_frames=True, frames=frames)

    # Copy the map to avoid modifying the original
    animated_map = [row[:] for row in map]

    # Find initial robot position
    start = next(((y, x) for y, line in enumerate(animated_map)
                  for x, char in enumerate(line) if char == '@'), None)

    # Walls and stones remain constant
    walls = extract_things(animated_map, '#')
    stones = extract_things(animated_map, 'O')

    # Move through each direction
    current_pos = start
    for move in moves:
        success, current_pos = move_robot(animated_map, current_pos, '@', move)
        render_map(animated_map, ax, save_frames=True, frames=frames)

    # Create animation
    def update(frame):
        ax.clear()
        ax.imshow(frames[frame], interpolation='nearest')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f'Warehouse Map - Move {frame}')
        return ax

    # Animate
    ani = animation.FuncAnimation(fig, update, frames=len(frames),
                                  interval=500, repeat=True)

    plt.show()

def move_robot(warehouse, pos, object, direction):
    next_pos = get_next_position(warehouse, pos, direction)
    if warehouse[next_pos[0]][next_pos[1]] == '#':
        return False, pos
    elif warehouse[next_pos[0]][next_pos[1]] in ('O','[',']'):
        is_possible, _ = move_robot(warehouse, next_pos, warehouse[next_pos[0]][next_pos[1]], direction)
        if is_possible:
            warehouse[next_pos[0]][next_pos[1]] = object
            if object == '@': warehouse[pos[0]][pos[1]] = '.'
            return True, next_pos
        else: return False, pos
    else:
        if object == '@': warehouse[pos[0]][pos[1]] = '.'
        warehouse[next_pos[0]][next_pos[1]] = object
        return True, next_pos

def move_robot_part2(warehouse, pos, object, direction):
    next_pos = get_next_position(warehouse, pos, direction)
    if warehouse[next_pos[0]][next_pos[1]] == '#':
        return False, pos
    elif warehouse[next_pos[0]][next_pos[1]] == '[':
        is_possible, _ = (move_robot(warehouse, next_pos, warehouse[next_pos[0]][next_pos[1]], direction)
                          and move_robot(warehouse, next_pos, warehouse[get_next_position(warehouse, pos, '>')[0]][get_next_position(warehouse, pos, '>')[1]], direction))
        if is_possible:
            warehouse[next_pos[0]][next_pos[1]] = object
            if object == '@': warehouse[pos[0]][pos[1]] = '.'
            return True, next_pos
        else: return False, pos
    elif warehouse[next_pos[0]][next_pos[1]] == ']':
        if direction == '>' or direction == '<':
            is_possible, _ = move_robot(warehouse, next_pos, warehouse[next_pos[0]][next_pos[1]], direction)
        else:
            is_possible, _ = (move_robot(warehouse, next_pos, warehouse[next_pos[0]][next_pos[1]], direction)
                              and move_robot(warehouse, next_pos, warehouse[get_next_position(warehouse, pos, '<')[0]][get_next_position(warehouse, pos, '<')[1]], direction))
        if is_possible:
            warehouse[next_pos[0]][next_pos[1]] = object
            if object == '@': warehouse[pos[0]][pos[1]] = '.'
            return True, next_pos
    else:
        if object == '@': warehouse[pos[0]][pos[1]] = '.'
        warehouse[next_pos[0]][next_pos[1]] = object
        return True, next_pos

map, moves = parse_input(EXAMPLE2)
start = next(find_start(map))
walls = extract_things(map, '#')
stones = extract_things(map, 'O')

def part1():
    next_pos = start
    for i, move in enumerate(moves):
        if move == '\n': continue
        _, next_pos = move_robot(map, next_pos, '@', move)
        animate_map(map, moves)

    def calculate_score(map):
        return sum((100*y+x) for y,row in enumerate(map) for x, value in enumerate(row) if value == 'O')

    print(f"Part1: {calculate_score(map)}")

def part2():
    next_pos = start
    for i, move in enumerate(moves):
        if move == '\n': continue
        _, next_pos = move_robot_part2(map, next_pos, '@', move)
        #animate_map(map, moves)

#part1()
part2()
