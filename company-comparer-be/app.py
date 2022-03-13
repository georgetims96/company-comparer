from flask import Flask, request
from flask_cors import CORS

# Import relevant views
from views.company_data import company_data
from views.company_search import company_search

app = Flask(__name__)
# Can delete when deployed
CORS(app)

# Register Blueprint for retrieving financial company data
app.register_blueprint(company_data, url_prefix='/company_data')

# Register Blueprint for retrieving company codes (i.e. CIK, ticker)
app.register_blueprint(company_search, url_prefix='/company_code')

if __name__ == "__main__":
    app.run(debug=True)