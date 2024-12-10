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

def invalid_rules(pages):
    invalid_pages = set()
    for page in pages:
        for i, x in enumerate(page):
            for y in page[i+1:]:
                if (y,x) in rules: invalid_pages.add(tuple(page))
                break
    return invalid_pages

def get_middle_page(pages):
    pages_count = []
    for i, x in enumerate(pages):
        pages_before, pages_after = 0, 0
        for y in pages:
            if (y,x) in rules:
                pages_before += 1
            if (x,y) in rules:
                pages_after += 1
        pages_count.append((x, pages_before, pages_after))
    return next(item[0] for item in pages_count if item[1] == item[2])

rules, updates = parse_input()
print(f"Part1: {sum(valide_rules(pages) for pages in updates)}")
print(f"Part2: {sum(get_middle_page(pages) for pages in invalid_rules(updates))}")
