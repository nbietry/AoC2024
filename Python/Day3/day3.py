import re

with open('input', 'r') as file:
    memory = file.read()

def evaluate_expression(op, arg1, arg2):
    operations = {
        "mul": lambda x ,y : int(x) * int(y)
    }
    return operations[op](int(arg1),int(arg2))

def part1(text):
    pattern = r'(mul|add|div)\((\d+),(\d+)\)'
    matches = re.findall(pattern, text)
    total = sum(evaluate_expression(m_op, m_arg1, m_arg2) for m_op,m_arg1,m_arg2 in matches)
    return total

def part2(text):
    pattern = r"(do\(\)|^)(.*?)(don't\(\)|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    total = sum(part1(m) for _, m, _ in matches)
    print(total)

print(part1(memory))
part2(memory)