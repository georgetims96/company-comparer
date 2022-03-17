import unittest
from models.company_financials import CompanyFinancials
class TestCOGS(unittest.TestCase):
    def test_cogs_MSFT(self):
        msft = CompanyFinancials.CompanyFinancials("0000789019")
        msft_cogs_data = msft.income_statement.determine_cogs()
        
        # Link: https://www.sec.gov/Archives/edgar/data/789019/000156459018019062/msft-10k_20180630.htm#ITEM_8_FINANCIAL_STATEMENTS_AND_SUPPLEM
        self.assertEqual(msft_cogs_data[2018], 38353000000, "Should be 38353000000")
        # Link: https://www.sec.gov/Archives/edgar/data/789019/000156459017014900/msft-10k_20170630.htm#ITEM_8_FINANCIAL_STATEMENTS_AND_SUPPLEM
        self.assertEqual(msft_cogs_data[2017], 34261000000, "Should be 38353000000")
    
    def test_cogs_NFLX(self):
        nflx = CompanyFinancials.CompanyFinancials("0001065280")
        nflx_cogs_data = nflx.income_statement.determine_cogs()
        
        # Link: https://www.sec.gov/Archives/edgar/data/1065280/000106528022000036/nflx-20211231.htm#i6247e85bf60945eebf3a8edf21e717c5_64
        self.assertEqual(nflx_cogs_data[2021], 17332683000, "Should be 17,332,683,000")
        # Link: https://www.sec.gov/Archives/edgar/data/1065280/000106528021000040/nflx-20201231.htm#ica2e9d6025314e8cacb7b361bd31b4d4_67
        self.assertEqual(nflx_cogs_data[2020], 15276319000, "Should be 15,276,319,000")
        # Link: https://www.sec.gov/Archives/edgar/data/1065280/000106528020000040/form10kq419.htm#sBCAE86991EC656FA9497E282C836684A
        self.assertEqual(nflx_cogs_data[2019], 12440213000, "Should be 12,440,213,000")
        # Link: https://www.sec.gov/Archives/edgar/data/1065280/000106528019000043/form10k_q418.htm#s8B618A29D9D15EDAA30C2E1F113A0040
        self.assertEqual(nflx_cogs_data[2018], 9967538000, "Should be 9,967,538")
        # Link: https://www.sec.gov/Archives/edgar/data/1065280/000162828018000941/q4nflx201710ka.htm#sDD6EE67F437E5E11832FDCDE52C76035


if __name__ == '__main__':
    unittest.main()


