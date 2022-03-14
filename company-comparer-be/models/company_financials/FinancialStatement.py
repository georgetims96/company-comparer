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
        Gets absolute financial data specified by a list of financial fields. Later entries in list will overwrite
        earlier entries if there two entries both have values for the sam year.

        :param financial_fields_to_check: financial fields as they appear in raw JSON
        :return: financial data from fields specified, one for each year prioritized as explained above and formatted {year : value}
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
    
    def get_annual_data(self, financial_field:str, year: int) -> int:
        """
        Returns financial data for specified financial field  and year

        :param financial_field: the financial field in the raw JSON from which we wish to pull
        :param year: the year for which we want the data
        :return: value of the financial field for the given year, if it exists; otherwise, None
        """
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
    
    def get_overlapping_years(self, fields: list) -> list:
        """
        Returns a list of the years for which we have data in the clean, absolute data for all fields specified

        :param fields: the financial fields we wish to check
        :return: the years for which we have data on all passed financial fields
        """
        years = []
        # Loop over financial fields provided
        for field in fields:
            # Add the years we have for the given financial field to the list
            years.append(self.absolute_fields[field].keys())
        # Get list of years for which we have comprehensive data
        overlapping_years = FinancialStatement.union_many(years)
        return overlapping_years
    
    def normalize_financial_data(self, overlapping_years: list, norm_financial_field: str, fields_to_normalize: list) -> dict:
        """
        Returns financial data for the passed years normalized using the specified normalizing financial field

        :param overlapping_years: years for which we want normalized data
        :param norm_financial_field: the financial field from the absolute data we'll use to normalize (i.e. divisor)
        :param fields_to_normalize: the financial fields from the absolute data that we'll normalize
        :return: normalized financial data in the format
        """
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
    
    def get_comprehensive_fields_years(self, financial_fields: list) -> list:
        """
        Returns a list of the years for which we have data in the raw JSON data for all fields specified

        :param financial_fields: the financial fields we wish to check
        :return: the years for which we have data on all passed financial fields
        """
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
        """
        Getter for normalized data

        :return: normalized data in the format {financial_field: {year : absolute_value}}
        """
        return self.normed_fields

    def get_absolute_data(self):
        """
        Getter for absolute data

        :return: absolute financial data in the format {financial_field: {year : relative_value}}
        """
        return self.absolute_fields

    @staticmethod
    def intersect_many(lists: list) -> list:
        """
        Returns elements that appear in all passed lists

        :param lists: list of lists whose intersection we'll return
        :return: list of elements that appear in all lists
        """
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
        """
        Returns all elements that appear in any of the passed lists

        :param lists: list of lists whose union we'll return
        :return: list of all elements that appear in any of the lists
        """
        # If there are no lists, return empty list
        if len(lists) == 0:
            return []
        else:
            union_set = set(lists[0])
            for i in range(1, len(lists)):
                union_set = union_set.union(set(lists[i]))
        return list(union_set)
    