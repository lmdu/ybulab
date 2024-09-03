import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ybulab.settings")

import django

if django.VERSION >= (1, 7):
	django.setup()

from specimen.models import Species

ss = []
with open('resources/animals.txt') as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')

		if cols[6] != 'Reptilia':
			continue

		ss.append(Species(
			species_en = cols[0], 
			species_cn = cols[1],
			kingdom_en = cols[2],
			kingdom_cn = cols[3],
			phylum_en = cols[4],
			phylum_cn = cols[5],
			class_en = cols[6],
			class_cn = cols[7],
			order_en = cols[8],
			order_cn = cols[9],
			family_en = cols[10],
			family_cn = cols[11],
			genus_en = cols[12],
			genus_cn = cols[13]
		))

Species.objects.bulk_create(ss)
