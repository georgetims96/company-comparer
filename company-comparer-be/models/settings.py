# Desired Financial Fields and their 10-K Equivalents

## Income Statement Fields
from tkinter import W


REVENUE_FIELDS = ['Revenue', 'SalesRevenueGoodsNet', 'SalesRevenueNet', 'Revenues', 'RevenueFromContractWithCustomerIncludingAssessedTax', 'RevenueFromContractWithCustomerExcludingAssessedTax']
COGS_FIELDS = ['CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization', 'CostOfGoodsSold', 'CostOfSales', 'CostOfServices', 'CostOfRevenue', 'CostOfGoodsAndServicesSold', 'CostOfGoodsAndServicesSold']
GROSS_PROFIT_FIELDS = ['GrossProfit']
SGA_FIELDS = ['GeneralAndAdministrativeExpense','SellingGeneralAndAdministrativeExpense']
SM_FIELDS = ['MarketingAndAdvertisingExpense', 'SellingAndMarketingExpense', 'MarketingExpense']
GA_FIELDS = ['GeneralAndAdministrativeExpense']
RD_FIELDS = ['ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost', 'ResearchAndDevelopmentExpenseSoftwareExcludingAcquiredInProcessCost', 'TechnologyandDevelopmentExpense', 'ResearchAndDevelopmentExpense']
OP_INC_FIELDS = ['IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments', 'ProfitLossFromOperatingActivities', 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest','OperatingIncomeLoss']

## Cash Flow Fields

### Net Income Adjustments
OPERATING_CASH_FLOW_FIELDS = ['NetCashProvidedByUsedInOperatingActivities']
DEPRECIATION_AMORTIZATION_FIELDS = ['DepreciationDepletionAndAmortization']
SHARE_BASED_COMPENSATION_FIELDS = ['ShareBasedCompensation']
DEFERRED_TAX_DELTA = ['DeferredIncomeTaxExpenseBenefit']

### Changes in Operating Assets and Liabilities
AR_DELTA_FIELDS = ['IncreaseDecreaseInAccountsReceivable']
INVENTORY_DELTA_FIELDS = ['IncreaseDecreaseInInventories']
OTHER_AR_DELTAS_FIELDS = ['IncreaseDecreaseInOtherReceivables']
AP_DELTA_FIELDS = ['IncreaseDecreaseInAccountsPayable']
DR_DELTA_FIELDS = ['IncreaseDecreaseInContractWithCustomerLiability']
OTHER_OP_CF_DELTA_FIELDS = ['IncreaseDecreaseInOtherOperatingLiabilities']

# Investing Activities

INVESTING_CASH_FLOW_FIELDS = ['NetCashProvidedByUsedInInvestingActivities']
PPE_CF_FIELDS = ['PaymentsToAcquirePropertyPlantAndEquipment']
PAYMENTS_TO_ACQUIRE_BUSINESSES_FIELDS = ['PaymentsToAcquireBusinessesNetOfCashAcquired']


# Relevant currency, filing type, and accounting standards

CURRENCY_FIELDS = ["USD", "EUR", "CAD", "GBP"]
ACCOUNTING_STANDARDS = ["us-gaap", "ifrs-full"]
ANNUAL_FORMS = ["10-K", "10-K/A", "20-F"]

# Ticker JSON file
TICKER_DATA_FILE = "./data/company_tickers.json"
