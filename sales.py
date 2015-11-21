import sqlite3 as lite
import sys

sales =(
	('Varsha', 22000),
	('Sulekha', 25000),
	('Priya', 28000),
	('Sandeep', 20000),
	('Rajesh', 29000),
	('Rajat', 18000),
	('Harshal', 25000),
	('Bhausaheb', 25000),
	('Kinjal', 19000),
	('Ananya', 29000),
	)

con = lite.connect('sales.db')

with con:
	cur = con.cursor()
	
	cur.execute("DROP TABLE IF EXISTS reps")
	cur.execute("CREATE TABLE reps(rep_name TEXT, amount INT)")
	cur.executemany("INSERT INTO reps VALUES(?, ?)", sales)