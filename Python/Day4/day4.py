puzzle = []
with open('input', 'r') as file:
    for line in file:
        puzzle.append(list(line))

def search_word(matrix, word):
    rows=len(matrix)
    cols=len(matrix[0])
    directions=[
        (0,1), #go right
        (1,0), #go down
        (1,1), #go diag right down
        (1,-1) #go diag left down
    ]

    def is_valid(x,y):
        return 0<=x<rows and 0<=y<cols

    def search_from_position(x,y,direction):
        dx, dy = direction
        current_word = ""
        for i in range(len(word)):
            nx, ny = x + i * dx, y + i * dy
            if not is_valid(nx, ny) or (matrix[nx][ny] != word[i] and matrix[nx][ny] != word[len(word)-1-i]):
                return False
            else:
                current_word = current_word + matrix[nx][ny]
        return current_word == "XMAS" or current_word == "SAMX"

    counter = 0
    for i in range(rows):
        for j in range(cols):
            for direction in directions:
                if search_from_position(i,j,direction):
                    counter+=1

    return counter
print(f"Part1: {search_word(puzzle, 'XMAS')}")

def search_cross_word(matrix):
    counter = 0
    for above, current, below in zip(puzzle, puzzle[1:], puzzle[2:]):
        for letters in zip(above, above[2:], current[1:], below, below[2:]):
            if "".join(letters) in ("MMASS", "MSAMS", "SMASM", "SSAMM"):
                counter += 1
    return counter
print(f"Part2: {search_cross_word(puzzle)}")




