import models.settings as settings
from typing import List

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
        self.comprehensive_years = []

        self.add_simple_financial_entry("revenue", settings.REVENUE_FIELDS, is_necessary=True)
        self.add_simple_financial_entry("cogs", settings.COGS_FIELDS)

        # Add Gross Margin
        self.add_computed_financial_entry("gross_margin", ["revenue - cogs"])

        # Normalize COGS
        self.add_normed_financial_entry("cogs", "revenue")
        self.add_normed_financial_entry("gross_margin", "revenue")
    
    def add_simple_financial_entry(self, name: str, financial_fields: List[str], is_necessary: bool=False) -> None:
        """
        Add a simple financial entry (i.e. not calculated) to the financial statement

        :param name: the name of the financial entry (i.e. "revenue")
        :param financial_fields: the potential keys for the financial fields in the 10-K
        :param necessary: whether we only want to return data for years that this financial data has (horrible english...)
        """
        # Filter out fields that don't appear in the 10-K
        filtered_fields = [x for x in financial_fields if x in self.raw_json['facts'][self.accounting_standard]]
        
        # Add the relevant financial data to the financial statement
        self.absolute_fields[name] = self.get_financial_data(filtered_fields)
        # Check if the financial entry must be included in the data returned to the user
        if is_necessary:
            # Check if this is the first financial entry to be added
            if not self.comprehensive_years:
                # If it is, set the comprehensive years equal to that of the current simple financial entry
                self.comprehensive_years = list(self.absolute_fields[name].keys())
            else:
                # If it isn't the first, we want to make sure the comprehensive years is correct
                new_years = set(self.comprehensive_years).intersection(set(self.absolute_fields[name].keys()))
                self.comprehensive_years = list(new_years)

    def add_computed_financial_entry(self, name: str, expressions: List[str]) -> None:
        """
        Adds a calculated financial entry field to the FinancialStatement. It tries each of the provided
        expressions for each of the relevant years, adding the first one that can be successfully computed

        :param name: The name of the calculated financial field. For example, 'gross_margin'
        :param expressions: A list of expressions to try. For example, 'gross_margin' could be 'revenue - cogs'
        """
        years_to_calc = self.comprehensive_years
        computed_entry_data = {}
        # For every relevant year
        for year in years_to_calc:
            # construct relevant variable map
            cur_year_map = {}
            # For every financial entry
            for entry in self.absolute_fields:
                # Check if we have data for the given year
                if year in self.absolute_fields[entry]:
                    # If we do, add it to the variable map at the correct point 
                    cur_year_map[entry] = self.absolute_fields[entry][year]
            # Once we've constructed the map, use it to calculate the current year value
            # We'll go expression by expression until we find the first valid one
            # for the current year
            # Once we have it, we'll break to move onto the next year
            for expression in expressions:
                try:
                    cur_year_data = eval(expression, cur_year_map)
                    computed_entry_data[year] = cur_year_data
                    break
                except:
                    continue
        # Save computed data
        self.absolute_fields[name] = computed_entry_data

    def add_normed_financial_entry(self, num: str, denom: str) -> None:
        """
        Adds normed financial entry to the FinancialStatement

        :param num: the name of the financial entry to be normalized (i.e. "cogs")
        :param denom: the name of the financial entry we will use to normalize (i.e. "revenue")
        """

        # Empty dictionary to store normalized data
        norm_company_data = {}
        
        # Loop over all relevant years
        for year in self.comprehensive_years:
            # If year isn't present for one of the entries, set year to "N/A"
            if year not in self.absolute_fields[num] or year not in self.absolute_fields[denom]:
                # Set that year to "N/A"
                norm_company_data[year] = "N/A"
            # Otherwise, we can normalize
            else:
                norm_company_data[year] = self.absolute_fields[num][year] / self.absolute_fields[denom][year]
        
        # Add normed data to FinancialStatement 
        self.normed_fields[num] = norm_company_data

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
            # FIXME what about 20-F?
            filtered_data = [x for x in self.raw_json['facts'][self.accounting_standard][financial_field]['units'][self.currency] \
                if x["form"] in settings.ANNUAL_FORMS]
            # Loop over all years for which we have 10-K filings
            for year in self.accns:
                # Get only financial entries for the current year
                year_data = [x for x in filtered_data if x['accn'] == self.accns[year] and x['fy'] == year]
                # Filter out interim/quarterly data
                # FIXME remove
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
    
    def get_accn_years(self) -> list:
        """
        Returns years for which we have 10-Ks

        FIXME not that some companies, like Darden have filings that are not being picked up currently.
        This needs to be rectified.
        """
        return list(self.accns.keys())


    def get_comprehensive_fields_years(self, financial_fields_to_check: list) -> list:
        """
        Gets absolute financial data specified by a list of financial fields. Later entries in list will overwrite
        earlier entries if there two entries both have values for the same year.

        :param financial_fields_to_check: financial fields as they appear in raw JSON
        :return: financial data from fields specified, one for each year prioritized as explained above and formatted {year : value}
        """
        # Empty shell for financial data to return
        year_set = set()
        filtered_financial_fields = [x for x in self.raw_json['facts'][self.accounting_standard] if x in financial_fields_to_check]
        # Loop through passed financial fields
        for field in filtered_financial_fields:
            years_in_field = self.raw_json['facts'][self.accounting_standard][field]['units'][self.currency]
            for year in years_in_field:
                if year['fp'] == "FY" and year["form"] in settings.ANNUAL_FORMS:
                    year_set.add(year['fy'])
        return list(year_set)
    
    def get_normed_data(self) -> dict:
        """
        Getter for normalized data

        :return: normalized data in the format {financial_field: {year : absolute_value}}
        """
        return self.normed_fields

    def get_absolute_data(self) -> dict:
        """
        Getter for absolute data

        :return: absolute financial data in the format {financial_field: {year : relative_value}}
        """
        return self.absolute_fields

    def get_comprehensive_years(self) -> list:
        return self.comprehensive_years

    def get_fields(self) -> list:
        return list(self.absolute_fields.keys())

    def generate_json(self) -> dict:
        json_to_return = {}
        json_to_return['absolute'] = self.absolute_fields
        json_to_return['norm'] = self.normed_fields
        return json_to_return

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