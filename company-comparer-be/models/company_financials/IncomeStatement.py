import models.settings as settings
from models.company_financials.FinancialStatement import FinancialStatement


class IncomeStatement(FinancialStatement):
    def __init__(self, raw_json: dict, accounting_standard:str, currency: str):
        """
        Construct an income statement

        :param raw_json: the raw company JSON data to be processed
        :param accounting_standard: the company's accounting standard
        :param currency: the company's reporting currency
        """
        super().__init__(raw_json, accounting_standard, currency)
        self.comprehensive_years = self.get_comprehensive_fields_years(settings.REVENUE_FIELDS)
        # Populate absolute data fields
        self.absolute_fields["revenue"] = self.determine_revenue()
        self.absolute_fields["cogs"] = self.determine_cogs()
        self.absolute_fields["grossprofit"] = self.determine_gross_profit()
        self.absolute_fields["sm"] = self.determine_sales_and_marketing()
        self.absolute_fields["ga"] = self.determine_general_and_administrative()
        self.absolute_fields["sga"] = self.determine_s_g_and_a()
        self.absolute_fields["rd"] = self.determine_r_and_d()
        self.absolute_fields["op"] = self.determine_op()

        # Populate normalized data fields
        # TODO this should be dynamic from a config file. It should group fields together by common denominator
        self.overlapping_years = self.get_overlapping_years(list(self.absolute_fields.keys()))
        self.normed_fields = self.normalize_financial_data(self.overlapping_years, "revenue", list(self.absolute_fields.keys()))

    def determine_revenue(self) -> dict:
        """
        Determines revenue given externally configured fields and instance's raw JSON data

        :return: company's absolute revenue data in {year : absolute_revenue} format
        """
        # SEC data is not clean and different companies refer to revenue differently
        # Below are the relevant permutations for revenue, with most common last (as the last overwrites the previous
        revenue_fields = settings.REVENUE_FIELDS
        # Filter out fields that aren't in provided raw dictionary
        revenue_fields = list(filter(lambda x: x in self.raw_json['facts'][self.accounting_standard], revenue_fields))
        # Pass these revenue fields to the get_financial_data function
        return self.get_financial_data(revenue_fields)
    
    def determine_cogs(self) -> dict:
        """
        Determines COGS given externally configured fields and instance's raw JSON data

        :return: company's absolute COGS data in {year : absolute_cogs} format
        """
        # Relevant permutations of COG fields
        cog_fields = settings.COGS_FIELDS
        # Filter out fields that aren't in provided raw company data
        cog_fields = list(filter(lambda x: x in self.raw_json['facts'][self.accounting_standard], cog_fields))
        return self.get_financial_data(cog_fields)
    
    '''
    Determines gross profit given externally configured fields and raw JSON data
    '''
    def determine_gross_profit(self) -> dict:
        gross_profit = {}
        gross_profit_fields = settings.GROSS_PROFIT_FIELDS
        # Filter out fields that aren't in provided raw company data
        gross_profit_fields = list(filter(lambda x: x in self.raw_json['facts'][self.accounting_standard], gross_profit_fields))
        # Do an initial population of gross profit
        if (len(list(gross_profit_fields)) != 0):
            gross_profit = self.get_financial_data(gross_profit_fields)
        # Now backfill the data
        for year in self.comprehensive_years:
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
                    year_revenue_field = self.get_annual_data(rev_field, year)
                    if year_revenue_field:
                        break
                for cogs_field in cogs_fields:
                    year_cogs_field = self.get_annual_data(cogs_field, year)
                    if year_cogs_field:
                        break
                if year_revenue_field and year_cogs_field:
                    gross_profit[year] = year_revenue_field - year_cogs_field
        return gross_profit

    '''
    Determines sales and marketing expense given externally configured fields and raw JSON data
    '''
    def determine_sales_and_marketing(self) -> dict:
        # Relevant S&M fields FIXME check marketing expense!!!!
        sales_and_marketing_fields = settings.SM_FIELDS
        sales_and_marketing_fields = list(filter(lambda x: x in self.raw_json['facts'][self.accounting_standard], sales_and_marketing_fields))
        # Pass these fields to the get_financial_data function
        return self.get_financial_data(sales_and_marketing_fields)
    
    '''
    Determines general and administrative expense given externally configured fields and raw JSON data
    '''
    def determine_general_and_administrative(self) -> dict:
        # Relevant G&A fields
        general_and_administrative_fields = settings.GA_FIELDS
        general_and_administrative_fields = list(filter(lambda x: x in self.raw_json['facts'][self.accounting_standard], general_and_administrative_fields))
        # Pass these fields to the get_financial_data function
        return self.get_financial_data(general_and_administrative_fields)

    '''
    Determines s,g&a expense given externally configured fields and raw JSON data
    '''
    def determine_s_g_and_a(self) -> dict:
        s_g_a = {}
        # Start by trying to add S&M and G&A
        for year in self.comprehensive_years:
            s_m_fields = settings.SM_FIELDS
            s_m_fields.reverse()
            g_a_fields = settings.GA_FIELDS
            g_a_fields.reverse()
            year_sm_field = ""
            year_ga_field = ""
            if year not in s_g_a:
                for s_m_field in s_m_fields:
                    year_sm_field = self.get_annual_data(s_m_field, year)
                    if year_sm_field:
                        break
                for g_a_field in g_a_fields:
                    year_ga_field = self.get_annual_data(g_a_field, year)
                    if year_ga_field:
                        break
                if year_sm_field and year_ga_field:
                    s_g_a[year] = year_sm_field + year_ga_field
        # Relevant SG&A fields
        s_g_a_fields = settings.SGA_FIELDS
        # Filter out fields that are not in 10-K
        s_g_a_fields = list(filter(lambda x: x in self.raw_json['facts'][self.accounting_standard], s_g_a_fields))
        s_g_a_collapsed = {}
        if len(s_g_a_fields) != 0:
            s_g_a_collapsed = self.get_financial_data(s_g_a_fields)
        for year in self.comprehensive_years:
            if year not in s_g_a and year in s_g_a_collapsed:
                s_g_a[year] = s_g_a_collapsed[year]
        '''
        FIXME After some testing, this should be safe to remove
        # Now backfill the data
        for year in self.comprehensive_years:
            s_m_fields = settings.SM_FIELDS
            s_m_fields.reverse()
            g_a_fields = settings.GA_FIELDS
            g_a_fields.reverse()
            year_sm_field = ""
            year_ga_field = ""
            if year not in s_g_a:
                for s_m_field in s_m_fields:
                    year_sm_field = self.get_annual_data(s_m_field, year)
                    if year_sm_field:
                        break
                for g_a_field in g_a_fields:
                    year_ga_field = self.get_annual_data(g_a_field, year)
                    if year_ga_field:
                        break
                if year_sm_field and year_ga_field:
                    s_g_a[year] = year_sm_field + year_ga_field
        '''
        return s_g_a
        

    '''
    Determines R&D expense given externally configured fields and raw JSON data
    '''
    def determine_r_and_d(self) -> dict:
        # Relevant R&D fields
        r_and_d_fields = settings.RD_FIELDS
        # Filter out fields that aren't in provided raw dictionary
        r_and_d_fields = list(filter(lambda x: x in self.raw_json['facts'][self.accounting_standard], r_and_d_fields))
        # Pass these fields to the get_financial_data function
        return self.get_financial_data(r_and_d_fields)

    def determine_op(self) -> dict:
        # Relevant Operating Income fields
        op_fields = settings.OP_INC_FIELDS
        op_fields = filter(lambda x: x in self.raw_json['facts'][self.accounting_standard], op_fields)
        # Pass these fields to the get_financial_data function
        return self.get_financial_data(op_fields)

    def get_comprehensive_years(self) -> list:
        return self.comprehensive_years

    def get_fields(self) -> list:
        return list(self.absolute_fields.keys())

    def generate_json(self) -> dict:
        json_to_return = {}
        json_to_return['absolute'] = self.absolute_fields
        json_to_return['norm'] = self.normed_fields
        return json_to_return
