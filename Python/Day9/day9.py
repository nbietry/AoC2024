INPUT_EXAMPLE = """
2333133121414131402
"""
def get_block_lists(disk_map):
    free_blocks = []
    file_blocks = []
    for i in range(len(disk_map)):
        if i % 2 == 0: # even indices are file blocks and odd are free blocks
            file_blocks.append(int(disk_map[i]))
        else:
            free_blocks.append(int(disk_map[i]))
    return file_blocks, free_blocks

def create_blocks(file_blocks, free_blocks):
    block_list = []
    for i in range(len(file_blocks)):
        block_list.append([str(i)] * file_blocks[i])
        if i < len(free_blocks):  # free_blocks list has 1 less element than file_blocks
            block_list.append(["."] * free_blocks[i])
    return [item for sublist in block_list for item in sublist]


def format_blocks(data: list):
    """
    >>> ''.join(format_blocks(list("0..111....22222")))
    '022111222......'
    >>> ''.join(format_blocks(list("00...111...2...333.44.5555.6666.777.888899")))
    '0099811188827773336446555566..............'
    """
    num_counter = len([char for char in data if char.isdigit()])
    non_dot_characters = [char for char in reversed(data) if char != '.']
    output = []
    for i, char in enumerate(data):
        if char == '.': char = non_dot_characters.pop(0)
        if i >= num_counter: char = '.'
        output.append(char)
    return output

def checkSum(block_list):
    result = 0
    for i, block in enumerate(block_list):
        if block != ".":
            result += i * int(block)
    return result

with open('input', 'r') as file:
    disk_map = file.read()
    disk_map = disk_map.rstrip('\n')

file_blocks, free_blocks = get_block_lists(disk_map)
print(f"Part1: {checkSum(format_blocks(create_blocks(file_blocks, free_blocks)))}")