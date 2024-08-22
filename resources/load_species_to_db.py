import sqlite3
conn = sqlite3.connect('../db.sqlite3')
cur = conn.cursor()
sql = "INSERT INTO specimen_species VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

rows = []
with open('animals.txt') as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		cols.insert(0, None)
		rows.append(cols)

cur.executemany(sql, rows)
conn.commit()
