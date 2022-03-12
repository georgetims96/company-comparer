import json
import sqlite3

# FIXME Need to figure out path stuff with flask
connection = sqlite3.connect('../data/cc.db')
cur = connection.cursor()
# Maybe pull at regular intervals from SEC rather than local? (https://www.sec.gov/files/company_tickers.json)
company_code_data = open('../data/company_tickers.json')

company_code_json = json.load(company_code_data)

'''
CREATE TABLE company_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    popularity INTEGER NOT NULL DEFAULT,
    cik TEXT NOT NULL,
    name TEXT NOT NULL
);
'''

def fill_zeros(cik: str) -> str:
    zeros_to_add = 10 - len(cik)
    return (zeros_to_add * "0") + cik
# FIXME really need to figure out if inserting alphabetically would be preferable...

# Loop through all company codes
for popularity in company_code_json:
    print(popularity)
    cur.execute("INSERT INTO company_codes (popularity, cik, ticker, company_name) VALUES (?, ?, ?, ?)",
    (int(popularity), fill_zeros(str(company_code_json[popularity]["cik_str"])), company_code_json[popularity]["ticker"], company_code_json[popularity]["title"].lower()))

#commit changes
connection.commit()
connection.close()

