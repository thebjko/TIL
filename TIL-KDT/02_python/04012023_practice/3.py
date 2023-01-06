from functools import reduce

number_list = [1,2,3,4,5]

sum = reduce(lambda x, y : x+y, number_list)
print(sum)