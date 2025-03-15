import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect(r"C:\Users\VIRUS\Desktop\UNIVERSAL\ve\my_test\database\blod.db")

cur =conn.cursor()
cur.execute("SELECT name from sqlite_master WHERE type='table';")
tables=cur.fetchall()

print ("Database Schema:\n")
for table in tables  :
    table_name =table[0]
    print(f"Schema for table :{table_name}")

    cur.execute (f"PRAGMA table_info({table_name});")
    columns=cur.fetchall()

    for column in columns :
        print(column)

conn.close()