with open('data/fruits.txt', 'r', encoding='UTF8') as f:
    lines = f.readlines()
    with open('data/02.txt', 'w', encoding='UTF8') as d:
        d.write(str(len(lines)))
