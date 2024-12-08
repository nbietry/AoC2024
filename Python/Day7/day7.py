import itertools
import re

# Test data
data = {
    190: [10, 19],
    3267: [81, 40, 27],
    83: [17, 5],
    156: [15, 6],
    7290: [6, 8, 6, 15],
    161011: [16, 10, 13],
    192: [17, 8, 14],
    21037: [9, 7, 18, 13],
    292: [11, 6, 16, 20],
}

def parse_input():
    data = []
    with open('input', 'r') as file:
        for line in file:
            numbers = list(map(int, re.findall(r'\d+', line)))
            if numbers:
                key = numbers[0]
                values = numbers[1:]
                data.append((key,values))
    return data

def generate_operations(numbers, operator_list):
    n = len(numbers) - 1
    return list(itertools.product(operator_list, repeat=n))

def evaluate_expression_left_to_right(expression):
    tokens = expression.split()
    result = int(tokens[0])
    i = 1
    while i < len(tokens):
        operator = tokens[i]
        number = int(tokens[i + 1])
        match operator:
            case '+': result += number
            case '*': result *= number
            case '||': result = int(str(result) + str(number))
        i += 2
    return result

def part1(data_file):
    total = 0
    for target, numbers in data_file:
        operations = generate_operations(numbers, ['+', '*'])
        for op in operations:
            expression = str(numbers[0])
            for i, num in enumerate(numbers[1::]):
                expression += " " + op[i] + " " + str(num)
            result = evaluate_expression_left_to_right(expression)
            #print(target, expression, result==target)
            if result == target:
                total += target
                break
    return total

def part2(data_file):
    total = 0
    for target, numbers in data_file:
        operations = generate_operations(numbers, ['+', '*', '||'])
        for op in operations:
            expression = str(numbers[0])
            for i, num in enumerate(numbers[1::]):
                expression += " " + op[i] + " " + str(num)
            result = evaluate_expression_left_to_right(expression)
            #print(target, expression, result==target)
            if result == target:
                total += target
                break
    return total

#print(f"Example: {part1(data)}")
print(f"Part1: {part1(parse_input())}")
print(f"Part2: {part2(parse_input())}")

