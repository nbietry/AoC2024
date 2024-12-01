list1 = []
list2 = []
with open('input1', 'r') as file:
    for line in file:
        values = line.split()
        list1.append(int(values[0]))
        list2.append(int(values[1]))


def part1():
    list1.sort()
    list2.sort()

    result = sum(abs(a - b) for a, b in zip(list1, list2))
    print(result)

def part2():
    result = sum(a*list2.count(a) for a in list1)
    print(result)

part1()
part2()