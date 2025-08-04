import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
"""
Scrape the web page https://it.wikipedia.org/wiki/Serie_A_2023-2024 containing
   the statistics of Serie A 2023-2024 in tabular format.
   Extract the content of the table containing the league standings and convert it to a DataFrame.
   Save the table in an Excel file called classifica_serieA_exercise7.xlsx
"""
url = "https://it.wikipedia.org/wiki/Serie_A_2023-2024"
response = urllib.request.urlopen(url)
html_content = response.read()
soup = BeautifulSoup(html_content, 'lxml')
# Extract the content of the table containing the league standings
classifica_table = soup.find('table', class_= 'wikitable sortable')

#Print the content of the table
for row in classifica_table.find_all('tr'):
    for cell in row.find_all(['th', 'td']):
        print(cell.get_text(strip = True), end = ' | ')
    print()
    
#Convert classifica_table to DataFrame and save to classifica_serieA_exercise7.xlsx
df_classifica = pd.read_html(str(classifica_table))
with pd.ExcelWriter('classifica_SERIEA_exercise7.xlsx') as writer:
    df_classifica[0].to_excel(writer, sheet_name = 'Classifica', index = False)
    
print("League table successfully saved in classifica_SERIEA_exercise7.xlsx")
    