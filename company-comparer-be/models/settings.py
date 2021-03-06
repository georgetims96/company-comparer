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
NET_INCOME_FIELDS = ['ProfitLoss', 'NetIncomeLossAvailableToCommonStockholdersBasic', 'NetIncomeLoss']
OPERATING_CASH_FLOW_FIELDS = ['CashFlowsFromUsedInOperatingActivities', 'NetCashProvidedByUsedInOperatingActivitiesContinuingOperations', 'NetCashProvidedByUsedInOperatingActivities']
# IFRS separates depreciation and amortization. Move first one to separate field
DEPRECIATION_AMORTIZATION_FIELDS = ['DepreciationAndAmortization', 'AdjustmentsForDepreciationExpense', 'DepreciationAmortizationAndOther', 'DepreciationAmortizationAndAccretionNet', 'DepreciationDepletionAndAmortization']
SHARE_BASED_COMPENSATION_FIELDS = ['AdjustmentsForSharebasedPayments', 'ShareBasedCompensation']
DEFERRED_TAX_DELTA = ['DeferredIncomeTaxExpenseBenefit']

### Changes in Operating Assets and Liabilities
AR_DELTA_FIELDS = ['AdjustmentsForDecreaseIncreaseInTradeAndOtherReceivables', 'IncreaseDecreaseInReceivables', 'IncreaseDecreaseInAccountsReceivableAndOtherOperatingAssets', 'IncreaseDecreaseInAccountsAndOtherReceivables', 'IncreaseDecreaseInAccountsReceivable']
INVENTORY_DELTA_FIELDS = ['IncreaseDecreaseInRetailRelatedInventories', 'IncreaseDecreaseInInventories']
OTHER_AR_DELTAS_FIELDS = ['IncreaseDecreaseInOtherReceivables']
AP_DELTA_FIELDS = ['AdjustmentsForIncreaseDecreaseInTradeAndOtherPayables', 'IncreaseDecreaseInAccountsPayable']
DR_DELTA_FIELDS = ['AdjustmentsForIncreaseDecreaseInDeferredIncomeIncludingContractLiabilities', 'IncreaseDecreaseInContractWithCustomerLiability']
OTHER_OP_CF_DELTA_FIELDS = ['IncreaseDecreaseInOtherOperatingLiabilities']

# Investing Activities

INVESTING_CASH_FLOW_FIELDS = ['CashFlowsFromUsedInInvestingActivities', 'NetCashProvidedByUsedInInvestingActivitiesContinuingOperations', 'NetCashProvidedByUsedInInvestingActivities']
PPE_CF_FIELDS = ['PurchasesOfPropertyAndEquipmentAndIntangibleAssets', 'PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities', 'PaymentsToAcquireProductiveAssets', 'PaymentsToAcquirePropertyPlantAndEquipment']
PAYMENTS_TO_ACQUIRE_BUSINESSES_FIELDS = ['CashFlowsUsedInObtainingControlOfSubsidiariesOrOtherBusinessesClassifiedAsInvestingActivities', 'PaymentsToAcquireBusinessesGross', 'PaymentsToAcquireBusinessesNetOfCashAcquired']
PAYMENTS_TO_DEVELOP_SOFTWARE_FIELDS = ['PaymentsToDevelopSoftware']

PURCHASE_OF_MARKETABLE_SECURITIES = ['PaymentsToAcquireAvailableForSaleSecuritiesDebt']
PROCEEDS_FROM_MARKETABLE_MATURITIES = ['ProceedsFromMaturitiesPrepaymentsAndCallsOfAvailableForSaleSecurities']
PROCEEDS_FROM_MARKETABLE_SALES = ['ProceedsFromSaleOfAvailableForSaleSecuritiesDebt']
PURCHASE_OF_NONMARKETABLE_SECURITIES = ['PaymentsToAcquireOtherInvestments']
PROCEEDS_FROM_NONMARKETABLE_SECURITIES = ['PaymentsToAcquireOtherInvestments']

# Relevant currency, filing type, and accounting standards

CURRENCY_FIELDS = ["USD", "EUR", "CAD", "GBP"]
ACCOUNTING_STANDARDS = ["us-gaap", "ifrs-full"]
ANNUAL_FORMS = ["10-K", "10-K/A", "20-F"]

# Ticker JSON file
TICKER_DATA_FILE = "./data/company_tickers.json"
