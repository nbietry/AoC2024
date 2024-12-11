def apply_rule(stone: str):
    """
    >>> apply_rule('125')
    '253000'
    >>> apply_rule('0')
    '1'
    >>> apply_rule('17')
    '1 7'
    """
    if stone == '0': return '1'
    elif len(stone) % 2 == 0: return ''.join((list(stone)[:len(stone) // 2])) + ' ' + ''.join(list(stone)[len(stone) // 2:])
    else: return str(int(stone) * 2024)


