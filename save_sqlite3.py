import sqlite3

conn = sqlite3.connect("top_cities.db")
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS cities")
c.execute(
    """
  CREATE TABLE cities (
    rank integer,
    city text,
    population integer
  )
"""
)

c.execute("INSERT INTO cities VALUES (?, ?, ?)", (1, "上海", 24150000))

c.execute("SELECT * FROM cities")
for row in c.fetchall():
    print(row)


conn.close()
