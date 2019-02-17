f1 = open('mapx_values.csv', 'r')
f2 = open('mapy_values.csv', 'r')

f3 = open('mapx_values_no_newlines.csv', 'w')
f4 = open('mapy_values_no_newlines.csv', 'w')

mapxStr = f1.read()
mapyStr = f2.read()

for ch in mapxStr:
	if ch != '\n':
		f3.write(ch)
	else:
		f3.write(',')

for ch in mapxStr:
	if ch != '\n':
		f4.write(ch)
	else:
		f4.write(',')