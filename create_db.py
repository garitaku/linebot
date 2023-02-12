import sqlite3
import csv
from random import choice
def create_db():
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    create_table = "CREATE TABLE IF NOT EXISTS test (id INTEGER, dajare TEXT, score TEXT)"
    cur.execute(create_table)#SQL実行

    open_csv=open("dajare.csv")
    read_csv=csv.reader(open_csv)

    next_row=next(read_csv)#先頭行スキップ
    rows=[]
    for row in read_csv:
        rows.append(row)
    cur.executemany("INSERT INTO test (id, dajare, score) VALUES (?, ?, ?)", rows)
    con.commit()
    open_csv.close()

    # select_test = "SELECT dajare FROM test WHERE dajare LIKE '%大佐%';"
    # cur.execute(select_test)
    # print(choice(cur.fetchall()))

# create_db()