from moon import moon

moon = moon()

ls = [*moon].remove('e')
print(''.join(ls))