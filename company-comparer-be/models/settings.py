# Desired Financial Fields and their 10-K Equivalents

REVENUE_FIELDS = ['Revenue', 'SalesRevenueNet', 'Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax']
COGS_FIELDS = ['CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization', 'CostOfSales', 'CostOfServices', 'CostOfRevenue', 'CostOfGoodsAndServicesSold']
GROSS_PROFIT_FIELDS = ['GrossProfit']
SGA_FIELDS = ['GeneralAndAdministrativeExpense','SellingGeneralAndAdministrativeExpense']
SM_FIELDS = ['MarketingAndAdvertisingExpense', 'SellingAndMarketingExpense', 'MarketingExpense']
GA_FIELDS = ['GeneralAndAdministrativeExpense']
RD_FIELDS = ['ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost', 'ResearchAndDevelopmentExpenseSoftwareExcludingAcquiredInProcessCost', 'TechnologyandDevelopmentExpense', 'ResearchAndDevelopmentExpense']
OP_INC_FIELDS = ['ProfitLossFromOperatingActivities', 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest','OperatingIncomeLoss']

# Relevant currency and accounting standards

CURRENCY_FIELDS = ["USD", "EUR", "CAD", "GBP"]
ACCOUNTING_STANDARDS = ["us-gaap", "ifrs-full"]

# Ticker JSON file
TICKER_DATA_FILE = "./data/company_tickers.json"