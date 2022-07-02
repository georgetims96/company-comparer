from flask import Blueprint
from models.company_financials.CompanyFinancials import CompanyFinancials

company_data = Blueprint('company_data', __name__)

@company_data.route('/<cik>')
def company_financial_data(cik):
    # Split request into individual companies
    individual_companies = cik.split("&")
    companies_json_data = []
    # Collect each of the company's requested JSON data
    for company in individual_companies:
        company_financials = CompanyFinancials(company)
        companies_json_data.append(company_financials)
    # Merge the data into a single JSON object
    dat_to_return = CompanyFinancials.merge_company_data(companies_json_data)
    # TODO replace this with logging
    # print(dat_to_return)
    return dat_to_return