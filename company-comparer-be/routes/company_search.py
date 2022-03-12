from flask import Blueprint
import sqlite3
import json

# FIXME Should this be here or in route?


company_search = Blueprint('company_search', __name__)

@company_search.route('/search/<search_query>')
def company_code_search(search_query):
    connection = sqlite3.connect('./db/data/cc.db')
    cur = connection.cursor()
    # Query the database given the provided search query
    cur.execute('SELECT * FROM company_codes WHERE company_name LIKE ? OR ticker LIKE ? LIMIT 10', ('%' + search_query.lower() +'%', '%' + search_query.upper() +'%'))
    search_results = []
    rows = cur.fetchall()
    for row in rows:
        search_results.append({
            "cik": row[2],
            "ticker": row[3],
            "name": row[4].title()
        })
        search_results[-1]
    data = {"search_results": search_results}
    return data