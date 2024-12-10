INPUT_EXAMPLE = """
2333133121414131402
"""

def format_blocks(data: list):
    """
    >>> format_blocks(list("0..111....22222"))
    '022111222......'
    >>> format_blocks(list("00...111...2...333.44.5555.6666.777.888899"))
    '0099811188827773336446555566..............'
    """
    num_counter = len([char for char in data if char.isdigit()])
    non_dot_characters = [char for char in reversed(data) if char != '.']
    output = []
    for i, char in enumerate(data):
        if char == '.': char = non_dot_characters.pop(0)
        if i >= num_counter: char = '.'
        output.append(char)
    return ''.join(output)

print(f"Part1: {format_blocks(list(open('input').read().strip()))}")