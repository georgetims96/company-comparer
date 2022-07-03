import requests
from models.company_financials.CashFlowStatement import CashFlowStatement
from models.company_financials.IncomeStatement import IncomeStatement
from models.company_financials.FinancialStatement import FinancialStatement
import models.settings as settings

class CompanyFinancials:
    def __init__(self, cik: str):
        """
        Construct a new CompanyFinancials object

        :param cik: The CIK of the company
        """
        self.cik = cik
        self.raw_json_data = CompanyFinancials.download_raw_json(cik)
        # Determine accounting standard for passed company
        self.accounting_standard = self.determine_accounting_standard()
        # Determine currency for passed company
        self.currency = self.determine_currency()
        self.accns = self.get_accns()
        self.income_statement = IncomeStatement(self.raw_json_data, self.accounting_standard, self.currency, self.accns)
        self.cash_flow_statement = CashFlowStatement(self.raw_json_data, self.accounting_standard, self.currency, self.accns)

    @staticmethod
    def download_raw_json(cik: str) -> dict:
        """
        Downloads and returns raw JSON data for a given company

        :param cik: The CIK for the company whose data we wish to pull
        :return: The raw JSON data for the company
        """
        headers = {'User-Agent': 'GWT george.tims@upenn.edu'}
        response = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)
        return response.json()
    
    def get_raw_json(self) -> dict:
        """
        Simple getter for raw JSON data

        :return: The raw JSON data for the company
        """
        return self.raw_json_data
    
    def determine_accounting_standard(self) -> str:
        """
        Determine the company's accounting standard

        :return: The company's accounting standard (i.e. GAAP, IFRS etc.)
        """
        # List of supported accounting standards
        # TODO should add to settings configurations
        potential_accounting_standards = settings.ACCOUNTING_STANDARDS
        for standard in potential_accounting_standards:
            if standard in self.raw_json_data['facts']: return standard

    def determine_currency(self) -> str:
        """
        Determine the company's currency

        :return: The company's reporting currency (i.e. USD, GBP etc. )
        """
        # List of supported currencies
        potential_currency_fields = settings.CURRENCY_FIELDS
        for field in self.raw_json_data['facts'][self.accounting_standard]:
            for currency in potential_currency_fields:
                if currency in self.raw_json_data['facts'][self.accounting_standard][field]['units']: return currency
    
    def get_accns(self) -> str:
        """
        Returns accn for 10-K filings, which will be useful for constructing links. N.B. that this replicates a lot of financial statment code.
        Could probably refactor

        :return: {year : accn}
        """
        # empty dictionary that will contain returned data
        financial_data = {}
        financial_fields_to_check = settings.OP_INC_FIELDS
        # Filter out fields that aren't in provided raw company data
        financial_fields_to_check = list(filter(lambda x: x in self.raw_json_data['facts'][self.accounting_standard], financial_fields_to_check))

        # Loop through provided financial fields
        for financial_field in financial_fields_to_check:
            # Filter so we only get annual filings
            annual_data = filter(lambda x: x['fp'] == "FY" and (x['form'] in settings.ANNUAL_FORMS), 
            self.raw_json_data['facts'][self.accounting_standard][financial_field]['units'][self.currency])
            # Unfortunately, this will still yield some garbage
            for filing in annual_data:
                # Filter out relevant numbers (len == 6 because we want CY2020 not CY2020Q1)
                #if 'frame' in filing and len(filing['frame']) == 6:
                    # FIXME MIGHT NEED TO CHANGE FINANCIAL DATA 
                financial_data[filing['fy']] = filing['accn']
        # Return the constructed dictionary
        return financial_data
       

    def generate_json(self) -> dict:
        """
        Generate the appropriately formated JSON that will contain the company's processed data

        :return: The company's financials in the correctly formatted JSON format for the front-end
        """
        json_to_return = {}
        json_to_return['error'] = ""
        json_to_return['data'] = {}
        json_to_return['data']['ciks'] = [self.cik]
        json_to_return['data']['years'] = self.income_statement.get_comprehensive_years()
        json_to_return['data']['fields'] = self.income_statement.get_fields()
        json_to_return['data'][self.cik] = {}
        json_to_return['data'][self.cik]['accn'] = self.get_accns()
        json_to_return['data'][self.cik]['is'] = {}
        json_to_return['data'][self.cik]['is']['norm'] = self.income_statement.get_normed_data()
        json_to_return['data'][self.cik]['is']['absolute'] = self.income_statement.get_absolute_data()
        
        json_to_return['data'][self.cik]['cf'] = {}
        json_to_return['data'][self.cik]['cf']['absolute'] = self.cash_flow_statement.get_absolute_data()
        json_to_return['data'][self.cik]['cf']['norm'] = self.cash_flow_statement.get_normed_data()

        return json_to_return
    
    @staticmethod
    def merge_company_data(company_data: list) -> dict:
        """
        Merges the passed companies' appropriately formatted JSON data
        
        :return: The companies' merged financial in the correctly formatted JSON format
        """
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
