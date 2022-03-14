from flask import Blueprint
from models.company_search.CompanySearchQuery import CompanySearchQuery

company_search = Blueprint('company_search', __name__)

@company_search.route('/search/<search_query>')
def company_code_search(search_query):
    search_entity = CompanySearchQuery(search_query, 10)
    data = {"search_results": search_entity.get_results()}
    return data