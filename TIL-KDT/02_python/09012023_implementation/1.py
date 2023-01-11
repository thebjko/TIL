from moon import moon

moon = moon()
if 'e' not in moon:
        print(-1)
else:
    for i, j in enumerate(moon):
        if j == 'e':
            print(i)
	    break
