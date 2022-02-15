from flask import Blueprint
from utils.company_data_helpers import *

company_data = Blueprint('company_data', __name__)


@company_data.route('/<cik>')
def company_financial_data(cik):
    # Split request into individual companies
    individual_companies = cik.split("&")
    companies_json_data = []
    for company in individual_companies:
        company_financials = CompanyFinancials(company, ["revenue", "cogs", "grossprofit", "sga", "sm", "ga", "rd", "op"])
        companies_json_data.append(company_financials)
    dat_to_return = merge_company_data(companies_json_data)
    return dat_to_return
    '''
    raw_company_data = get_raw_company_data(cik)
    clean_company_data = {}
    clean_company_data['revenue'] = get_revenue(raw_company_data)
    clean_company_data['cogs'] = get_cogs(raw_company_data)
    clean_company_data['sga'] = get_s_g_and_a(raw_company_data)
    norm_financial_data = normalize_financial_data(clean_company_data, "revenue", ["revenue", "cogs", "sga"])
    norm_financial_data["years"] = sorted(norm_financial_data['revenue'].keys())
    return norm_financial_data
    '''