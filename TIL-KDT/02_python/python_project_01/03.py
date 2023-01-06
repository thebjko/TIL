with open('data/fruits.txt', 'r', encoding='UTF8') as f:
    lines = f.readlines()
    my_set = set()

    with open('data/03.txt', 'w', encoding='UTF8') as d:
        for line in lines:
            line = line.strip()
            if line[-5:] == 'berry':
                my_set.add(line)
        d.write(f'{len(my_set)}\n')
        d.write('\n'.join(my_set))
    
    # print(len(my_set), '\n', '\n'.join(my_set), sep='')

# how to count unique values in list - https://datagy.io/python-count-unique-values-list/
# how to overwrite a file - https://favtutor.com/blogs/overwrite-file-python