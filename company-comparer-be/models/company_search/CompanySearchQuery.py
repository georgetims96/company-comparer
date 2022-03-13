import json
import models.settings as settings

class CompanySearchQuery:
    """
    Construct a company search query

    :param search_text: the query text
    :param results_limit: the maximum number of results to return 
    """
    def __init__(self, search_text: str, results_limit: int):
        self.search_text = search_text.lower()
        self.results_limit = results_limit
        self.file_source = settings.TICKER_DATA_FILE
        self.results = self.perform_search()
    
    def perform_search(self) -> list:
        """
        Searches company tickers JSON file for relevant entries

        :return: list of search results, structured as required by front-end
        """
        with open(self.file_source) as f:
            data = json.load(f)
        companyKeys = data.keys()
        i = 0
        results = []
        # TODO rewrite using enumerate 
        for key in companyKeys:
            if i >= self.results_limit: break
            if self.search_text in data[key]['ticker'].lower() or self.search_text in data[key]['title'].lower():
                company_entity = {}
                company_entity["cik"] = self.fill_zeros(data[key]['cik_str'])
                company_entity["ticker"] = data[key]['ticker']
                company_entity["name"] = data[key]["title"].title()
                results.append(company_entity)
                i += 1
        print(results)
        return results
    
    def fill_zeros(self, cik: str) -> str:
        """
        Fills a CIK code with zeroes to be the correct length for the SEC API call

        :param cik: the CIK code to pad
        :return: the padded CIK code
        """
        zeros_to_add = 10 - len(str(cik))
        return (zeros_to_add * "0") + str(cik)
    
    def get_results(self) -> list:
        """
        Simple getter for the results of a search query

        :return: the results of the search query
        """
        return self.results
