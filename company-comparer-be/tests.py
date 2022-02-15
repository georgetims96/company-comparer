import json

'''
# https://data.sec.gov/api/xbrl/companyfacts/CIK0001326801.json
        # secURL = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
        headers = {'User-Agent': 'GWT george.tims@upenn.edu'}
        response = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)
        return response.json()
https://data.sec.gov/api/xbrl/companyfacts/CIK0001639920.json"
        0001639920
        raw_company_data['facts']['us-gaap'][financial_field]['units']['USD']
'''

class FinancialEntity:
    '''
    Holds financial data for a given entity for every findable time period in a
    a provided JSON document

    '''
    _possible_accounting_standards = ['us-gaap']

    def __init__(self, json_to_process: dict,  possible_values: list,
    accounting_standard="us-gaap", currency="USD", backfill=True):
        '''
        Parameters
        ----------
        json_to_process : dict
            The company financial data in JSON forma
        possible_values : list
            The keys in the JSON doc that might contain the data we want. Order indicates priority
        backfill : bool
            If multiple possible values are present in the document, we backfill when the the top
            value is not present if true
        '''
        self._json_to_process = json_to_process
        self._backfill = backfill
        self._possible_values = possible_values
        # FIXME change
        self._accounting_standard = accounting_standard
        self._currency = currency
        # FIXME need to determine report as well
        self._filtered_values = self.filter_fields()
        self._data = self.get_annual_data()

    def filter_fields(self):
        '''
        Figures out which values are actually in the 10-K

        Returns
        -------
        list
            list of financial fields that are 
        '''

        filtered_fields = filter(lambda x: x in self._json_to_process['facts'][self._accounting_standard]
        , self._possible_values)
        filtered_values = list(filtered_fields)
        if len(filtered_values) > 0 and not self._backfill:
            return [filtered_values[0]]
        else:
            return filtered_values

    def get_annual_data(self):
        '''
        Returns a dictionary of data. Keys are years, with data as values

        Returns
        -------
        dict
            dictionary of annual financial data
        '''
        # FIXME looks like we don't need to specify difference between 10-K 20-F etc???
        # Need to reverse financial fields to maintain priority
        financial_fields_to_check = list(reversed(self._filtered_values))
        financial_data = {}
        # Loop through provided financial fields
        for financial_field in financial_fields_to_check:
            # Filter so we only get annual filings
            annual_data = filter(lambda x: x['fp'] == "FY", 
            self._json_to_process['facts'][self._accounting_standard][financial_field]['units'][self._currency])
            # Unfortunately, this will still yield some garbage
            for filing in annual_data:
                # Filter out relevant numbers (len == 6 because we want CY2020 not CY2020Q1)
                if 'frame' in filing and len(filing['frame']) == 6:
                    financial_data[int(filing['frame'][2:])] = filing['val']
        # Return the constructed dictionary
        return financial_data

    def __repr__(self):
        str_to_ret = ""
        for year in self._data:
            str_to_ret = str(str_to_ret) + str(year)+ ": " + str(self._data[year]) + "\n"
        return str_to_ret


f = open("./data/companyfacts/CIK0000320193.json")
data = json.load(f)
print("hello")
revenue = FinancialEntity(data, ['SalesRevenueNet', 'Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax'])
cogs = FinancialEntity(data, )
print(revenue)