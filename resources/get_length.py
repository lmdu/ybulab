lens = [0] * 14
with open('animals.txt') as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')

		for i, col in enumerate(cols):
			if len(col) > lens[i]:
				lens[i] = len(col)

print(*lens, sep='\t')
