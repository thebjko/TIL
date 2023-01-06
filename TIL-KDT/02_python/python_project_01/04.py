with open('data/fruits.txt', 'r', encoding='UTF8') as f:
    lines = f.readlines()
    fruits_count = dict()
    for line in lines:
        line = line.strip()
        if line in fruits_count:
            fruits_count[line] += 1
        else:
            fruits_count[line] = 1
    with open('data/04.txt', 'w', encoding='UTF8') as d:
        for fruit in fruits_count:    
            d.write(f'{fruit} {fruits_count[fruit]}\n')
