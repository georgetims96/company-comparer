from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'GWT george.tims@upenn.edu'}
accounting_text = requests.get("https://www.sec.gov/Archives/edgar/data/1075531/000107553121000019/R10.htm", headers=headers).text
my_soup = BeautifulSoup(accounting_text, 'html.parser')
accounting_policies = my_soup.find_all(class_="text")
with open("../scrape_result.html", "w") as file:
    file.write(str(accounting_policies))
print(accounting_policies)