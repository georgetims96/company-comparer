import models.settings as settings
from models.company_financials.FinancialStatement import FinancialStatement


class IncomeStatement(FinancialStatement):
    def __init__(self, raw_json: dict, accounting_standard:str, currency: str, accns: dict):
        """
        Construct an income statement

        :param raw_json: the raw company JSON data to be processed
        :param accounting_standard: the company's accounting standard
        :param currency: the company's reporting currency
        """
        super().__init__(raw_json, accounting_standard, currency, accns)
        # TODO Might want to replace with revenue years i.e.
        
        self.comprehensive_years = []
        
        # Populate absolute data fields
        self.add_simple_financial_entry("revenue", settings.REVENUE_FIELDS, is_necessary=True)
        self.add_simple_financial_entry("cogs", settings.COGS_FIELDS)
        self.add_simple_financial_entry("grossprofit", settings.GROSS_PROFIT_FIELDS)
        self.add_simple_financial_entry("sm", settings.SM_FIELDS)
        self.add_simple_financial_entry("ga", settings.GA_FIELDS)
        self.add_simple_financial_entry("sga", settings.SGA_FIELDS)
        self.add_simple_financial_entry("rd", settings.RD_FIELDS)
        self.add_simple_financial_entry("op", settings.OP_INC_FIELDS)

        # Add computed fields
        self.add_computed_financial_entry("grossprofit", ["grossprofit", "revenue - cogs"])
        self.add_computed_financial_entry("sga", ["sm + ga", "sga"])
        self.add_computed_financial_entry("other", ["revenue-cogs-sga-rd-op"])

        # add normed fields
        self.add_normed_financial_entry("revenue", "revenue")
        self.add_normed_financial_entry("revenue", "revenue")
        self.add_normed_financial_entry("grossprofit", "revenue")
        self.add_normed_financial_entry("sm", "revenue")
        self.add_normed_financial_entry("ga", "revenue")
        self.add_normed_financial_entry("sga", "revenue")
        self.add_normed_financial_entry("rd", "revenue")
        self.add_normed_financial_entry("op", "revenue")
