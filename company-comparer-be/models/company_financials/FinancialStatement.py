import models.settings as settings
class FinancialStatement:
    def __init__(self, raw_json: dict, accounting_standard: str, currency: str, accns: dict):
        """
        Constructor for financial statement superclass

        :param raw_json: the raw company JSON data to be processed
        :param accounting_standard: the company's accounting standard
        :param currency: the company's reporting currency
        """
        self.raw_json = raw_json
        self.accounting_standard = accounting_standard
        self.currency = currency
        self.accns = accns
        self.absolute_fields = {}
        self.normed_fields = {}
    
    def get_financial_data(self, financial_fields_to_check: list, attrib:str ='val') -> dict:
        """
        Gets absolute financial data specified by a list of financial fields. Later entries in list will overwrite
        earlier entries if there two entries both have values for the same year.

        :param financial_fields_to_check: financial fields as they appear in raw JSON
        :return: financial data from fields specified, one for each year prioritized as explained above and formatted {year : value}
        """
        # Empty shell for financial data to return
        financial_data = {}
        # Loop through passed financial fields
        for financial_field in financial_fields_to_check:
            # Filter out non-10-K forms
            filtered_data = [x for x in self.raw_json['facts'][self.accounting_standard][financial_field]['units'][self.currency] if x["form"] == "10-K" or x["form"] == "10-K/A"]
            # Loop over all years for which we have 10-K filings
            for year in self.accns:
                # Get only financial entries for the current year
                year_data = [x for x in filtered_data if x['accn'] == self.accns[year] and x['fy'] == year]
                # Filter out interim/quarterly data
                year_data = [x for x in year_data if FinancialStatement.days_apart(x['start'], x['end']) > 300]
                # If we have at least one entry remaining
                if year_data:
                    # Get the latest entry (i.e. the entry for the most recent fiscal year)
                    max_entry = year_data[0]
                    for entry in year_data:
                        if int(entry['start'].split('-')[0]) > int(max_entry['start'].split('-')[0]):
                            max_entry = entry
                    # And set the relevant year in our shell to return to the value at the entry's specified attribute
                    financial_data[year] = max_entry[attrib]
        # Return the financial data
        return financial_data
    
    def get_annual_data(self, financial_field:str, year: int, attrib:str ='val') -> int:
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
                return filing[attrib]
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
                    # year_set.add(int(year['frame'][2:]))
                    year_set.add(year['fy'])

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
    
    @staticmethod
    def days_apart(start_date, end_date):
        start_split = start_date.split('-')
        end_split = end_date.split('-')
        start_val = int(start_split[0]) * 365 + int(start_split[1]) * 30 + int(start_split[2])
        end_val = int(end_split[0]) * 365 + int(end_split[1]) * 30 + int(end_split[2])
        return end_val - start_val
    