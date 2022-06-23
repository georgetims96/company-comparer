# Desired Financial Fields and their 10-K Equivalents

## Income Statement Fields
from tkinter import W


REVENUE_FIELDS = ['Revenue', 'SalesRevenueGoodsNet', 'SalesRevenueNet', 'Revenues', 'RevenueFromContractWithCustomerIncludingAssessedTax', 'RevenueFromContractWithCustomerExcludingAssessedTax']
COGS_FIELDS = ['CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization', 'CostOfGoodsSold', 'CostOfSales', 'CostOfServices', 'CostOfRevenue', 'CostOfGoodsAndServicesSold']
GROSS_PROFIT_FIELDS = ['GrossProfit']
SGA_FIELDS = ['GeneralAndAdministrativeExpense','SellingGeneralAndAdministrativeExpense']
SM_FIELDS = ['MarketingAndAdvertisingExpense', 'SellingAndMarketingExpense', 'MarketingExpense']
GA_FIELDS = ['GeneralAndAdministrativeExpense']
RD_FIELDS = ['ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost', 'ResearchAndDevelopmentExpenseSoftwareExcludingAcquiredInProcessCost', 'TechnologyandDevelopmentExpense', 'ResearchAndDevelopmentExpense']
OP_INC_FIELDS = ['ProfitLossFromOperatingActivities', 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest','OperatingIncomeLoss']

## Cash Flow Fields

### Net Income Adjustments
OPERATING_CASH_FLOW_FIELDS = ['NetCashProvidedByUsedInOperatingActivities']
DEPRECIATION_AMORTIZATION_FIELDS = ['DepreciationDepletionAndAmortization']
SHARE_BASED_COMPENSATION_FIELDS = ['ShareBasedCompensation']
DEFERRED_TAX_DELTA = ['DeferredIncomeTaxExpenseBenefit']

### Changes in Operating Assets and Liabilities
AR_DELTA = ['IncreaseDecreaseInAccountsReceivable']
INVENTORY_DELTA = ['IncreaseDecreaseInInventories']
OTHER_AR_DELTA = ['IncreaseDecreaseInOtherReceivables']
AP_DELTA = ['IncreaseDecreaseInAccountsPayable']
DR_DELTA = ['IncreaseDecreaseInContractWithCustomerLiability']


# Relevant currency, filing type, and accounting standards

CURRENCY_FIELDS = ["USD", "EUR", "CAD", "GBP"]
ACCOUNTING_STANDARDS = ["us-gaap", "ifrs-full"]
ANNUAL_FORMS = ["10-K", "10-K/A", "20-F"]

# Ticker JSON file
TICKER_DATA_FILE = "./data/company_tickers.json"