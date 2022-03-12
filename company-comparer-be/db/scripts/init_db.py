import sqlite3

connection = sqlite3.connect('../data/cc.db')


with open('../schema/company_codes_schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()