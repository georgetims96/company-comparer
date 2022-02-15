from curses import raw
import requests
import settings


class CompanyFinancials:
    def __init__(self, cik: str, financial_fields: list):
        # Check for errors!!!!!
        self.__financial_functions = {
        "revenue": CompanyFinancials.get_revenue,
        "cogs": CompanyFinancials.get_cogs,
        "grossprofit": CompanyFinancials.get_gross_profit,
        "sga": CompanyFinancials.get_s_g_and_a,
        "sm": CompanyFinancials.get_sales_and_marketing,
        "ga": CompanyFinancials.get_general_and_administrative,
        "rd": CompanyFinancials.get_r_and_d,
        "op": CompanyFinancials.get_op,
        }
        self.cik = cik
        self.raw_company_data = CompanyFinancials.get_raw_company_data(self.cik)
        self.accounting_standard = CompanyFinancials.determine_accounting_standard(self.raw_company_data)
        self.currency = CompanyFinancials.determine_currency(self.raw_company_data, self.accounting_standard)
        # FIXME REMOVE!!!!
        self.financial_fields = financial_fields
        self.comprehensive_years = CompanyFinancials.get_comprehensive_revenue_years(self.raw_company_data, self.accounting_standard, self.currency)
        # Initialize and populate company's original (clean) financial data 
        self.absolute_data = {}
        self.populate_financial_data()
        self.norm_data = {}
        self.normalize_fields()
        self.json_to_return = {}
        self.generate_json()
    
    def populate_financial_data(self):
        # Loop through provided financial fields and populate absolute data accordingly
        for field in self.financial_fields:
            # Call the function from above. We should probably put this in the class
            self.absolute_data[field] = self.__financial_functions[field](self.raw_company_data, self.accounting_standard, self.currency,
            self.comprehensive_years)
        # TODO Maybe provide a default?
    
    def populate_comprehensive_years(self, fields=None):
        if not fields:
            self.comprehensive_years = CompanyFinancials.get_comprehensive_years(self.absolute_data, self.financial_fields)

    def normalize_fields(self):
        # TODO: NEED MULTIPLE OPTIONS FOR THIS
        self.norm_data = CompanyFinancials.normalize_financial_data(self.absolute_data, "revenue", self.financial_fields)
    
    def generate_json(self):
        self.json_to_return["error"] = ""
        self.json_to_return["data"] = {}
        self.json_to_return["data"]["ciks"] = [self.cik]
        self.json_to_return["data"]["years"] = self.comprehensive_years
        self.json_to_return["data"]["fields"] = self.financial_fields
        self.json_to_return["data"][self.cik] = {}
        self.json_to_return["data"][self.cik]["norm"] = self.norm_data
        self.json_to_return["data"][self.cik]["absolute"] = self.absolute_data
        self.json_to_return
    
    def get_json(self):
        print(self.json_to_return)
        return self.json_to_return
    
    '''
    Returns raw company data from SEC companyfacts API given provided CIK

    @param: cik     CIK for company for which we want data

    @return raw company data from SEC API call
    '''
    @staticmethod
    def get_raw_company_data(cik: str) -> dict:
        # https://data.sec.gov/api/xbrl/companyfacts/CIK0001326801.json
        # secURL = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
        headers = {'User-Agent': 'GWT george.tims@upenn.edu'}
        response = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)
        return response.json()
    
    '''
    Returns specified financial fields from provided raw company JSON (i.e. dict) on an annual basis

    @param: raw_company_data            data returned from SEC API call
    @param: financial_fields_to_check   the financial fields we want to extract

    @return: returns the annual data for the specified fields 
    '''
    @staticmethod
    def get_financial_data(raw_company_data: dict, financial_fields_to_check: list, accounting_standard: str, currency: str) -> dict:
        # empty dictionary that will contain returned data
        financial_data = {}
        # Loop through provided financial fields
        for financial_field in financial_fields_to_check:
            # Filter so we only get annual filings
            annual_data = filter(lambda x: x['fp'] == "FY", 
            raw_company_data['facts'][accounting_standard][financial_field]['units'][currency])
            # Unfortunately, this will still yield some garbage
            for filing in annual_data:
                # Filter out relevant numbers (len == 6 because we want CY2020 not CY2020Q1)
                if 'frame' in filing and len(filing['frame']) == 6:
                    financial_data[int(filing['frame'][2:])] = filing['val']
        # Return the constructed dictionary
        return financial_data
    
    '''
    Doesn't assume you've checked field is there
    '''
    @staticmethod
    def get_annual_data(raw_company_data: dict, financial_field:str, year: int, accounting_standard: str, 
    currency:str) -> int:
        # FIXME shouldn't this have already been filtered in the calling functions?
        if financial_field not in raw_company_data['facts'][accounting_standard]:
            return None
        annual_data = filter(lambda x: x['fp'] == "FY", 
        raw_company_data['facts'][accounting_standard][financial_field]['units'][currency])
        # Unfortunately, this will still yield some garbage
        for filing in annual_data:
            # Filter out relevant numbers (len == 6 because we want CY2020 not CY2020Q1)
            if 'frame' in filing and len(filing['frame']) == 6 and filing['frame'] == 'CY' + str(year):
                return filing['val']
        return None
    
    @staticmethod
    def determine_accounting_standard(raw_company_data:dict):
        potential_accounting_standards = ["us-gaap", "ifrs-full"]
        for standard in potential_accounting_standards:
            if standard in raw_company_data['facts']: return standard

    @staticmethod
    def determine_currency(raw_company_data:dict, accounting_standard:str):
        # raw_company_data['facts'][accounting_standard][financial_field]['units'][currency]
        potential_currency_fields = ["USD", "EUR", "CAD", "GBP"]
        for field in raw_company_data['facts'][accounting_standard]:
            for currency in potential_currency_fields:
                if currency in raw_company_data['facts'][accounting_standard][field]['units']: return currency

    @staticmethod
    def get_revenue(raw_company_data: dict, accounting_standard:str, currency:str, years_to_backfill: list=None) -> dict:
        # SEC data is not clean and different companies refer to revenue differently
        # Below are the relevant permutations for revenue, with most common last (as the last overwrites the previous
        revenue_fields = settings.REVENUE_FIELDS
        # Filter out fields that aren't in provided raw dictionary
        revenue_fields = filter(lambda x: x in raw_company_data['facts'][accounting_standard], revenue_fields)
        # Pass these revenue fields to the get_financial_data function
        return CompanyFinancials.get_financial_data(raw_company_data, revenue_fields, accounting_standard, currency)
    
    @staticmethod
    def get_cogs(raw_company_data: dict, accounting_standard:str, currency:str, years_to_backfill: list=None)->dict:
        # Relevant permutations of COG fields
        cog_fields = settings.COGS_FIELDS
        # Filter out fields that aren't in provided raw company data
        cog_fields = list(filter(lambda x: x in raw_company_data['facts'][accounting_standard], cog_fields))
        return CompanyFinancials.get_financial_data(raw_company_data, cog_fields, accounting_standard, currency)
    
    @staticmethod
    def get_gross_profit(raw_company_data: dict, accounting_standard:str, currency:str, years_to_backfill: list)->dict:
        gross_profit = {}
        gross_profit_fields = settings.GROSS_PROFIT_FIELDS
        # Filter out fields that aren't in provided raw company data
        gross_profit_fields = list(filter(lambda x: x in raw_company_data['facts'][accounting_standard], gross_profit_fields))
        # Do an initial population of gross profit
        if (len(list(gross_profit_fields)) != 0):
            gross_profit = CompanyFinancials.get_financial_data(raw_company_data, gross_profit_fields, accounting_standard, currency)
        # Now backfill the data
        for year in years_to_backfill:
            # FIXME move to settings.py
            revenue_fields = settings.REVENUE_FIELDS
            revenue_fields.reverse()
            # FIXME same as above
            cogs_fields = settings.COGS_FIELDS
            cogs_fields.reverse()
            year_revenue_field = ""
            year_cogs_field = ""
            if year not in gross_profit:
                for rev_field in revenue_fields:
                    year_revenue_field = CompanyFinancials.get_annual_data(raw_company_data, rev_field, year, accounting_standard, currency)
                    if year_revenue_field:
                        break
                for cogs_field in cogs_fields:
                    year_cogs_field = CompanyFinancials.get_annual_data(raw_company_data, cogs_field, year, accounting_standard, currency)
                    if year_cogs_field:
                        break
                if year_revenue_field and year_cogs_field:
                    gross_profit[year] = year_revenue_field - year_cogs_field
        return gross_profit
        
    @staticmethod
    def get_s_g_and_a(raw_company_data: dict, accounting_standard: str, currency:str, years_to_backfill:list=None) -> dict:
        # Create empty s_g_a object
        s_g_a = {}
        # Relevant SG&A fields
        s_g_a_fields = settings.SGA_FIELDS
        # Filter out fields that are not in 10-K
        s_g_a_fields = list(filter(lambda x: x in raw_company_data['facts'][accounting_standard], s_g_a_fields))
        if len(s_g_a_fields) != 0:
            s_g_a = CompanyFinancials.get_financial_data(raw_company_data, s_g_a_fields, accounting_standard, currency)
        # Now backfill the data
        for year in years_to_backfill:
            s_m_fields = settings.SM_FIELDS
            s_m_fields.reverse()
            g_a_fields = settings.GA_FIELDS
            g_a_fields.reverse()
            year_sm_field = ""
            year_ga_field = ""
            if year not in s_g_a:
                for s_m_field in s_m_fields:
                    year_sm_field = CompanyFinancials.get_annual_data(raw_company_data, s_m_field, year, accounting_standard, currency)
                    if year_sm_field:
                        break
                for g_a_field in g_a_fields:
                    year_ga_field = CompanyFinancials.get_annual_data(raw_company_data, g_a_field, year, accounting_standard, currency)
                    if year_ga_field:
                        break
                if year_sm_field and year_ga_field:
                    s_g_a[year] = year_sm_field + year_ga_field
        return s_g_a
    
    @staticmethod
    def get_sales_and_marketing(raw_company_data: dict, accounting_standard:str, currency: str, years_to_backfill:list=None) -> dict:
        # Relevant S&M fields FIXME check marketing expense!!!!
        sales_and_marketing_fields = settings.SM_FIELDS
        sales_and_marketing_fields = list(filter(lambda x: x in raw_company_data['facts'][accounting_standard], sales_and_marketing_fields))
        # Pass these fields to the get_financial_data function
        return CompanyFinancials.get_financial_data(raw_company_data, sales_and_marketing_fields, accounting_standard, currency)

    @staticmethod
    def get_general_and_administrative(raw_company_data: dict, accounting_standard:str, currency:str, years_to_backfill:list=None) -> dict:
        # Relevant G&A fields
        general_and_administrative_fields = settings.GA_FIELDS
        general_and_administrative_fields = list(filter(lambda x: x in raw_company_data['facts'][accounting_standard], general_and_administrative_fields))
        # Pass these fields to the get_financial_data function
        return CompanyFinancials.get_financial_data(raw_company_data, general_and_administrative_fields, accounting_standard, currency)
    
    @staticmethod
    def get_r_and_d(raw_company_data: dict, accounting_standard:str, currency:str, years_to_backfill:list=None) -> dict:
        # Relevant R&D fields
        r_and_d_fields = settings.RD_FIELDS
        # Filter out fields that aren't in provided raw dictionary
        r_and_d_fields = filter(lambda x: x in raw_company_data['facts'][accounting_standard], r_and_d_fields)
        # Pass these fields to the get_financial_data function
        return CompanyFinancials.get_financial_data(raw_company_data, r_and_d_fields, accounting_standard, currency)
    
    @staticmethod
    def get_op(raw_company_data: dict, accounting_standard:str, currency:str, years_to_backfill:list=None) -> dict:
        # Relevant Operating Income fields
        op_fields = settings.OP_INC_FIELDS
        op_fields = filter(lambda x: x in raw_company_data['facts'][accounting_standard], op_fields)
        # Pass these fields to the get_financial_data function
        return CompanyFinancials.get_financial_data(raw_company_data, op_fields, accounting_standard, currency)

    @staticmethod
    def normalize_financial_data(clean_company_data: dict, norm_financial_field: str, fields_to_normalize: list) -> dict:
        # Will store normalized company data
        norm_company_data = {}
        # List of lists of years for each financial field
        overlapping_years = CompanyFinancials.get_comprehensive_years(clean_company_data, fields_to_normalize)
        # Loop over provided financial fields
        for field in fields_to_normalize:
            # Set up the dictionary for the current field
            norm_company_data[field] = {}
            # Loop through the overlapping years
            for year in overlapping_years:
                # If year not present, set to N/A
                if year not in clean_company_data[field] or year not in clean_company_data[norm_financial_field]:
                    norm_company_data[field][year] = "N/A"
                # Normalize company data based on provided field
                else:
                    norm_company_data[field][year] = clean_company_data[field][year] / clean_company_data[norm_financial_field][year]
        # Return the normed data
        return norm_company_data

    @staticmethod
    def get_comprehensive_years(clean_company_data: dict, fields: list) -> list:
        years = []
        # Loop over financial fields provided
        for field in fields:
            # Add the years we have for the given financial field to the list
            years.append(clean_company_data[field].keys())
        # Get list of years for which we have comprehensive data
        overlapping_years = CompanyFinancials.union_many(years)
        return overlapping_years
    
    '''
    Gets all years for which we have revenue data. This is an alternative to the old method of getting comprehensive years

    '''
    @staticmethod
    def get_comprehensive_revenue_years(raw_company_data, accounting_standard:str, currency:str) -> list:
        # SEC data is not clean and different companies refer to revenue differently
        # Below are the relevant permutations for revenue, with most common last (as the last overwrites the previous
        revenue_fields = settings.REVENUE_FIELDS
        # Filter out fields that aren't in provided raw dictionary
        revenue_fields = filter(lambda x: x in raw_company_data['facts'][accounting_standard], revenue_fields)
        # Populate list with all revenue years we have
        year_set = set()
        for field in revenue_fields:
            years_in_field = raw_company_data['facts'][accounting_standard][field]['units'][currency]
            for year in years_in_field:
                if 'frame' in year and len(year['frame']) == 6:
                    year_set.add(int(year['frame'][2:]))

        # Return list of revenue years
        return list(year_set)
    
    @staticmethod
    def intersect_many(lists: list) -> list:
        # If there are no lists, return empty list
        if len(lists) == 0:
            return []
        else:
            intersection_set = set(lists[0])
            for i in range(1, len(lists)):
                intersection_set = intersection_set.intersection(set(lists[i]))
        return list(intersection_set)
    
    @staticmethod
    def union_many(lists: list) -> list:
        # If there are no lists, return empty list
        if len(lists) == 0:
            return []
        else:
            union_set = set(lists[0])
            for i in range(1, len(lists)):
                union_set = union_set.union(set(lists[i]))
        return list(union_set)
    


def merge_company_data(company_data: list) -> dict:
    # Check to see that company data is provided
    if company_data == []: return {"error": "No company data instances passed!", "data": {}}

    merged_company_data = company_data[0].get_json()
    for i in range(1, len(company_data)):
        company_to_merge_json = company_data[i].get_json()
        merged_company_data["data"]["ciks"] += company_to_merge_json["data"]["ciks"]
        overlapping_years = CompanyFinancials.intersect_many([merged_company_data["data"]["years"], company_to_merge_json["data"]["years"]])
        merged_company_data["data"]["years"] = overlapping_years
        overlapping_fields = CompanyFinancials.intersect_many([merged_company_data["data"]["fields"], company_to_merge_json["data"]["fields"]])
        merged_company_data["data"]["fields"] = overlapping_fields
        merged_company_data["data"][company_to_merge_json["data"]["ciks"][0]] = company_to_merge_json["data"][company_to_merge_json["data"]["ciks"][0]]

    return merged_company_data

# META pull
'''
meta_raw_data = get_raw_company_data("0001326801")
meta_clean_data = {}
meta_clean_data["revenue"] = get_revenue(meta_raw_data)
meta_clean_data["cogs"] = get_cogs(meta_raw_data)
meta_clean_data["sg&a"] = get_s_g_and_a(meta_raw_data)
'''

# https://data.sec.gov/api/xbrl/companyfacts/CIK0001326801.json