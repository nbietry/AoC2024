EXAMPLE = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

def parse_input(data: str):
    return [list(line) for line in data.strip().splitlines()]

def get_start_positions(topo: [[]]):
    return [(y, x) for y in range(len(topo)) for x in range(len(topo[y])) if topo[y][x] == '0']

def bfs(topo: [[]], start_pos: (int, int)):
    visited = set()
    target_found = set()
    queue = [start_pos]
    while queue:
        y, x = queue.pop(0)
        if (y, x) in visited: continue
        visited.add((y, x))
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < len(topo) and 0 <= nx < len(topo[ny]) and int(topo[ny][nx]) == int(topo[y][x]) + 1:
                queue.append((ny, nx))
                if topo[ny][nx] == '9': target_found.add((ny, nx))
    return target_found

topo_map = parse_input(open("input").read())
start_pos = get_start_positions(topo_map)
print(sum(len(bfs(topo_map, pos)) for pos in start_pos))
