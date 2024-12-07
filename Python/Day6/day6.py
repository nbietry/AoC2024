from operator import truediv

directions = {
    "up": (-1, 0),
    "right": (0, 1),
    "down": (1, 0),
    "left": (0, -1)
}


def parse_input(data: str):
    guard_init = None
    obstruction_list = []
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            match char:
                case "^":
                    guard_init = (y, x)
                case "#":
                    obstruction_list.append((y, x))
    return obstruction_list, (y + 1, len(line)), guard_init


def move_guard(guard_pos, direction, obstacles):
    keys = list(directions.keys())
    original_direction = direction

    while (guard_pos[0] + directions[direction][0], guard_pos[1] + directions[direction][1]) in obstacles:
        current_index = keys.index(direction)
        direction = keys[(current_index + 1) % len(keys)]
        if direction == original_direction:
            # Break if we've tried all directions
            return guard_pos, direction, False

    new_pos = (guard_pos[0] + directions[direction][0], guard_pos[1] + directions[direction][1])
    return new_pos, direction, True


def part1(data: str):
    lab_visited_cells = set()
    obs_list, lab_size, guard_pos = parse_input(data)

    current_direction = "up"

    while 0 <= guard_pos[0] < lab_size[0] and 0 <= guard_pos[1] < lab_size[1]:
        lab_visited_cells.add(guard_pos)
        guard_pos, current_direction, moved = move_guard(guard_pos, current_direction, obs_list)
        if not moved:
            break

    print(len(lab_visited_cells))

def read_input():
    with open('input', 'r') as file:
        return file.read()

def check_candidate(guard_pos, direction, visited_cells, obstacles):
    # Check for obstacles and boundaries
    def is_path_clear(start, end, delta):
        current = start
        while current != end:
            if current in obstacles:
                return False
            next_y = current[0] + delta[0]
            next_x = current[1] + delta[1]
            current = (next_y, next_x)
        return True

    delta_y, delta_x  = directions[direction]

    # Iterate over all visited cells to find a matching column or row with the same direction
    for (visited_pos, visited_direction) in visited_cells:
        if visited_direction == direction:
            if direction in ("up", "down"):
                if ((direction == "down" and guard_pos[0] < visited_pos[0]) or (direction == "up" and guard_pos[0] > visited_pos[0])) and guard_pos[1] == visited_pos[1] and is_path_clear(guard_pos, visited_pos, (delta_y, 0)):
                    return True
            elif direction in ("left", "right"):
                # Check same row
                if ((direction == "right" and guard_pos[1] < visited_pos[1]) or (direction == "left" and guard_pos[1] > visited_pos[1])) and guard_pos[0] == visited_pos[0] and is_path_clear(guard_pos, visited_pos, (0, delta_x)):
                    return True
    return False

def part2(data):
    lab_visited_cells = []
    obs_list, lab_size, guard_pos = parse_input(data)

    current_direction = "up"
    direction_keys = list(directions.keys())
    candidate_loop = []

    while 0 <= guard_pos[0] < lab_size[0] and 0 <= guard_pos[1] < lab_size[1]:
        current_direction_index = direction_keys.index(current_direction)
        right_direction = direction_keys[(current_direction_index + 1) % len(direction_keys)]
        if check_candidate(guard_pos, right_direction, lab_visited_cells, obs_list):
            candidate_loop.append(
                (guard_pos[0] + directions[current_direction][0], guard_pos[1] + directions[current_direction][1])
            )
        if (guard_pos, current_direction) not in lab_visited_cells:
            lab_visited_cells.append((guard_pos,current_direction))
        guard_pos, current_direction, moved = move_guard(guard_pos, current_direction, obs_list)
        if not moved:
            break
    print(len(candidate_loop))

part1(read_input())
part2(read_input())