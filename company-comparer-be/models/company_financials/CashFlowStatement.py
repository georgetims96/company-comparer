import models.settings as settings
from models.company_financials.FinancialStatement import FinancialStatement


class CashFlowStatement(FinancialStatement):
    def __init__(self, raw_json: dict, accounting_standard:str, currency: str, accns: dict):
        """
        Construct an cash flow statement

        :param raw_json: the raw company JSON data to be processed
        :param accounting_standard: the company's accounting standard
        :param currency: the company's reporting currency
        """
        super().__init__(raw_json, accounting_standard, currency, accns)

        # self.comprehensive_years = self.get_comprehensive_fields_years(settings.REVENUE_FIELDS)
        self.comprehensive_years = []

        # Populate absolute data fields
        # N.B. Revenue and operating income are just as denominators
        self.add_simple_financial_entry("revenue", settings.REVENUE_FIELDS, is_necessary=True)
        self.add_simple_financial_entry("op_inc", settings.OP_INC_FIELDS)
        
        # Operating cash flow items
        self.add_simple_financial_entry("cfo", settings.OPERATING_CASH_FLOW_FIELDS)
        self.add_simple_financial_entry("da", settings.DEPRECIATION_AMORTIZATION_FIELDS)
        self.add_simple_financial_entry("sbc", settings.SHARE_BASED_COMPENSATION_FIELDS)
        self.add_simple_financial_entry("ar_delta", settings.AR_DELTA_FIELDS)
        self.add_simple_financial_entry("inv_delta", settings.INVENTORY_DELTA_FIELDS)
        self.add_simple_financial_entry("ap_delta", settings.AP_DELTA_FIELDS)
        self.add_simple_financial_entry("dr_delta", settings.AP_DELTA_FIELDS)

        # Investing cash flow items
        self.add_simple_financial_entry("cfi", settings.INVESTING_CASH_FLOW_FIELDS)

        self.add_normed_financial_entry("cfo", "revenue")
        self.add_normed_financial_entry("da", "revenue")
        self.add_normed_financial_entry("sbc", "revenue")
        self.add_normed_financial_entry("ar_delta", "revenue")
        self.add_normed_financial_entry("inv_delta", "revenue")
        self.add_normed_financial_entry("ap_delta", "revenue")

        self.add_normed_financial_entry("cfi", "revenue")