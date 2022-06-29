import models.settings as settings
from models.company_financials.FinancialStatement import FinancialStatement


class CashFlowStatement(FinancialStatement):
    def __init__(self, raw_json: dict, accounting_standard:str, currency: str, accns: dict):
        """
        Construct an income statement

        :param raw_json: the raw company JSON data to be processed
        :param accounting_standard: the company's accounting standard
        :param currency: the company's reporting currency
        """
        super().__init__(raw_json, accounting_standard, currency, accns)
        # TODO Might want to replace with revenue years i.e.
        # self.comprehensive_years = self.get_comprehensive_fields_years(settings.REVENUE_FIELDS)
        self.comprehensive_years = self.get_accn_years()
        # Populate absolute data fields
        self.absolute_fields["cfo"] = self.determine_cfo()
        self.absolute_fields["da"] = self.determine_da()
        self.absolute_fields["grossprofit"] = self.determine_gross_profit()
        self.absolute_fields["sbc"] = self.determine_sbc()
        self.absolute_fields["ga"] = self.determine_general_and_administrative()
        self.absolute_fields["sga"] = self.determine_s_g_and_a()
        self.absolute_fields["rd"] = self.determine_r_and_d()
        self.absolute_fields["op"] = self.determine_op()

        # Populate normalized data fields
        # TODO this should be dynamic from a config file. It should group fields together by common denominator
        self.overlapping_years = self.get_overlapping_years(list(self.absolute_fields.keys()))
        self.normed_fields = self.normalize_financial_data(self.overlapping_years, "revenue", list(self.absolute_fields.keys()))

    def determine_cfo(self) -> dict:
        """
        Determines operating cash flow given externally configured fields and instance's raw JSON data

        :return: company's absolute operating cash flow data in {year : absolute_operating_cash_flow} format
        """
        # SEC data is not clean and different companies refer to CFO differently
        # Below are the relevant permutations for CFO, with most common last (as the last overwrites the previous)
        cfo_fields = settings.OPERATING_CASH_FLOW_FIELDS
        # Filter out fields that aren't in provided raw dictionary
        cfo_fields = list(filter(lambda x: x in self.raw_json['facts'][self.accounting_standard], cfo_fields))
        # Pass these cfo fields to the get_financial_data function
        return self.get_financial_data(cfo_fields)
    
    def determine_da(self) -> dict:
        """
        Determines D&A given externally configured fields and instance's raw JSON data

        :return: company's absolute D&A data in {year : absolute_da} format
        """
        # Relevant permutations of D&A fields
        da_fields = settings.DEPRECIATION_AMORTIZATION_FIELDS
        # Filter out fields that aren't in provided raw company data
        da_fields = list(filter(lambda x: x in self.raw_json['facts'][self.accounting_standard], da_fields))
        # FIXME just return 
        return self.get_financial_data(da_fields)
    
    def determine_sbc(self) -> dict:
        '''
        Determines share-based compensation given externally configured fields and raw JSON data 

        :return: company's absolute share-based comp in {year : absolute_sbc} format
        '''
        # Relevant permutations of SBC fields
        sbc_fields = settings.SHARE_BASED_COMPENSATION_FIELDS
        # Filter out fields that aren't in provided raw company data
        sbc_fields = list(filter(lambda x: x in self.raw_json['facts'][self.accounting_standard], sbc_fields))
        # FIXME just return 
        return self.get_financial_data(sbc_fields)
        

    # FIXME: MOVE BELOW TO SUPERCLASS
    def get_comprehensive_years(self) -> list:
        return self.comprehensive_years

    def get_fields(self) -> list:
        return list(self.absolute_fields.keys())

    def generate_json(self) -> dict:
        json_to_return = {}
        json_to_return['absolute'] = self.absolute_fields
        json_to_return['norm'] = self.normed_fields
        return json_to_return
