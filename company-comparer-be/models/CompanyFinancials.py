import requests
from models.IncomeStatement import IncomeStatement
from models.FinancialStatement import FinancialStatement

class CompanyFinancials:
    def __init__(self, cik: str):
        self.cik = cik
        self.raw_json_data = CompanyFinancials.download_raw_json(cik)
        # Determine accounting standard for passed company
        self.accounting_standard = self.determine_accounting_standard()
        # Determine currency for passed company
        self.currency = self.determine_currency()
        self.income_statement = IncomeStatement(self.raw_json_data, self.accounting_standard, self.currency)

    @staticmethod
    def download_raw_json(cik: str) -> dict:
        headers = {'User-Agent': 'GWT george.tims@upenn.edu'}
        response = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)
        return response.json()
    
    def get_raw_json(self) -> dict:
        return self.raw_json_data
    
    def determine_accounting_standard(self) -> str:
        # List of supported accounting standards
        # TODO should add to settings configurations
        potential_accounting_standards = ["us-gaap", "ifrs-full"]
        for standard in potential_accounting_standards:
            if standard in self.raw_json_data['facts']: return standard

    def determine_currency(self) -> str:
        # List of supported currencies
        # TODO should add to settings configuration
        potential_currency_fields = ["USD", "EUR", "CAD", "GBP"]
        for field in self.raw_json_data['facts'][self.accounting_standard]:
            for currency in potential_currency_fields:
                if currency in self.raw_json_data['facts'][self.accounting_standard][field]['units']: return currency
    
    def generate_json(self) -> dict:
        json_to_return = {}
        json_to_return['error'] = ""
        json_to_return['data'] = {}
        json_to_return['data']['ciks'] = [self.cik]
        json_to_return['data']['years'] = self.income_statement.get_comprehensive_years()
        json_to_return['data']['fields'] = self.income_statement.get_fields()
        json_to_return['data'][self.cik] = {}
        json_to_return['data'][self.cik]['norm'] = self.income_statement.get_normed_data()
        json_to_return['data'][self.cik]['absolute'] = self.income_statement.get_absolute_data()
        return json_to_return
    
    @staticmethod
    def merge_company_data(company_data: list) -> dict:
    # Check to see that company data is provided
        if company_data == []: return {"error": "No company data instances passed!", "data": {}}

        merged_company_data = company_data[0].generate_json()
        for i in range(1, len(company_data)):
            company_to_merge_json = company_data[i].generate_json()
            merged_company_data["data"]["ciks"] += company_to_merge_json["data"]["ciks"]
            overlapping_years = FinancialStatement.intersect_many([merged_company_data["data"]["years"], company_to_merge_json["data"]["years"]])
            merged_company_data["data"]["years"] = overlapping_years
            overlapping_fields = FinancialStatement.intersect_many([merged_company_data["data"]["fields"], company_to_merge_json["data"]["fields"]])
            merged_company_data["data"]["fields"] = overlapping_fields
            merged_company_data["data"][company_to_merge_json["data"]["ciks"][0]] = company_to_merge_json["data"][company_to_merge_json["data"]["ciks"][0]]

        return merged_company_data
