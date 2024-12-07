def parse_input():
    data = open('input', 'r').read()
    (rules, updates) = data.split("\n\n")
    rules = {
        tuple(int(page) for page in line.split("|")) for line in rules.splitlines()
    }
    updates = [
        [int(page) for page in line.split(",")] for line in updates.splitlines()
    ]
    return rules, updates

def valide_rules(pages):
    for i, x in enumerate(pages):
        for y in pages[i+1:]:
            if (y,x) in rules: return 0
    return pages[len(pages)//2]

rules, updates = parse_input()
print(f"Part1: {sum(valide_rules(pages) for pages in updates)}")

def sort_update(pages):
    pass