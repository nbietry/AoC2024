import re

EXAMPLE="""p=2,4 v=2,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

def parse_input(data: str):
    robots=[]
    velocity=[]
    for line in data.splitlines():
        pattern = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"
        match = re.match(pattern, line)
        if match:
            px, py, vx, vy = map(int, match.groups())
            robots.append((px, py))
            velocity.append((vx, vy))
    return robots, velocity

def move_robot(robot, vel, width, high):
    pos = ((robot[0]+vel[0]) % width, (robot[1]+vel[1]) % high)
    for _ in range(99):
        pos = ((pos[0]+vel[0]) % width, (pos[1]+vel[1]) % high)
    return pos

robots, velocity = parse_input(open("input").read())

w, h = 101, 103
final_position = []
for i, robot in enumerate(robots):
    move_robot(robot, velocity[i], w, h)
    final_position.append(move_robot(robot, velocity[i], w, h))

Q1 = len([(x,y) for x, y in final_position if x < w//2 and y < h//2 ])
Q2 = len([(x,y) for x, y in final_position if w//2 < x < w and y < h//2 ])
Q3 = len([(x,y) for x, y in final_position if x < w//2 and h//2 < y < h ])
Q4 = len([(x,y) for x, y in final_position if w//2 < x < w and h//2 < y < h ])

print(final_position)
print(Q1*Q2*Q3*Q4)