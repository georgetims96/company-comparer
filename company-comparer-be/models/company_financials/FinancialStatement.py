class FinancialStatement:
    def __init__(self, raw_json: dict, accounting_standard: str, currency: str):
        """
        Constructor for financial statement superclass

        :param raw_json: the raw company JSON data to be processed
        :param accounting_standard: the company's accounting standard
        :param currency: the company's reporting currency
        """
        self.raw_json = raw_json
        self.accounting_standard = accounting_standard
        self.currency = currency
        self.absolute_fields = {}
        self.normed_fields = {}
    
    def get_financial_data(self, financial_fields_to_check: list) -> dict:
        """
        Gets financial data 
        """
        # empty dictionary that will contain returned data
        financial_data = {}
        # Loop through provided financial fields
        for financial_field in financial_fields_to_check:
            # Filter so we only get annual filings
            annual_data = filter(lambda x: x['fp'] == "FY", 
            self.raw_json['facts'][self.accounting_standard][financial_field]['units'][self.currency])
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
    def get_annual_data(self, financial_field:str, year: int) -> int:
        # FIXME shouldn't this have already been filtered in the calling functions?
        if financial_field not in self.raw_json['facts'][self.accounting_standard]:
            return None
        annual_data = filter(lambda x: x['fp'] == "FY", 
        self.raw_json['facts'][self.accounting_standard][financial_field]['units'][self.currency])
        # Unfortunately, this will still yield some garbage
        for filing in annual_data:
            # Filter out relevant numbers (len == 6 because we want CY2020 not CY2020Q1)
            if 'frame' in filing and len(filing['frame']) == 6 and filing['frame'] == 'CY' + str(year):
                return filing['val']
        return None
    
    '''
    FIXME need to think of a clever way of dealing with clean company data
    '''
    def get_overlapping_years(self, fields: list) -> list:
        years = []
        # Loop over financial fields provided
        for field in fields:
            # Add the years we have for the given financial field to the list
            years.append(self.absolute_fields[field].keys())
        # Get list of years for which we have comprehensive data
        overlapping_years = FinancialStatement.union_many(years)
        return overlapping_years
    
    '''
    FIXME need to improve this
    '''
    def normalize_financial_data(self, overlapping_years: list, norm_financial_field: str, fields_to_normalize: list) -> dict:
        # Will store normalized company data
        norm_company_data = {}
        # Loop over provided financial fields
        for field in fields_to_normalize:
            # Set up the dictionary for the current field
            norm_company_data[field] = {}
            # Loop through the overlapping years
            for year in overlapping_years:
                # If year not present, set to N/A
                if year not in self.absolute_fields[field] or year not in self.absolute_fields[norm_financial_field]:
                    norm_company_data[field][year] = "N/A"
                # Normalize company data based on provided field
                else:
                    norm_company_data[field][year] = self.absolute_fields[field][year] / self.absolute_fields[norm_financial_field][year]
        # Return the normed data
        return norm_company_data
    
    '''
    Gets all years for which we have specified list of field data. This is an alternative to the old method of getting comprehensive years.
    By default, we'll use revenue

    '''
    def get_comprehensive_fields_years(self, financial_fields: list) -> list:
        # SEC data is not clean and different companies refer to revenue differently
        # Filter out fields that aren't in provided raw dictionary
        financial_fields = filter(lambda x: x in self.raw_json['facts'][self.accounting_standard], financial_fields)
        # Populate list with all revenue years we have
        year_set = set()
        for field in financial_fields:
            years_in_field = self.raw_json['facts'][self.accounting_standard][field]['units'][self.currency]
            for year in years_in_field:
                if 'frame' in year and len(year['frame']) == 6:
                    year_set.add(int(year['frame'][2:]))

        # Return list of fields' years
        return list(year_set)
    
    def get_normed_data(self):
        return self.normed_fields

    def get_absolute_data(self):
        return self.absolute_fields

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
    