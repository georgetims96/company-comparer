import sqlite3

connection = sqlite3.connect('cc.db')


with open('./models/company_codes_schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()