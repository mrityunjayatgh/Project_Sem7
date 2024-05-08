import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from openpyxl.workbook import Workbook

now = datetime.now()
timestamp = now.strftime("%Y%m%d%H%M%S%f")[:-3]
file_name = f'data_{timestamp}.xlsx'

url = 'https://books.toscrape.com/'

# Fetch the webpage content
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the h3 tags containing book titles and extract their links
book_links = [book.a['href'] for book in soup.find_all('h3')]

# Add base URL if the links are relative
base_url = 'https://books.toscrape.com/'
book_links = [base_url + link if 'catalogue' in link else link for link in book_links]

# print(book_links)
for url1 in book_links:
    response1 = requests.get(url1)
    soup1 = BeautifulSoup(response1.text, 'html.parser')
    # title = soup.find('h1').text.strip()
    td_tags = soup1.find_all('td')

    # Extracting data from td tags
    data = [tag.text.strip() for tag in td_tags]
    # data.insert(0, title)

    # Create a DataFrame with the data
    df = pd.DataFrame([data], columns=[f"Column_{i+1}" for i in range(len(data))])
    headers = ['ID', 'Type', 'Price(Excluding Tax)', 'Price(Including Tax)', 'Tax', 'Availability', 'Reviews']
    # print(df)
    # Save the DataFrame to an Excel file
    if url1 == book_links[0]:
        df.to_excel(file_name, index=False, header=headers)
    else:
        df_old = pd.read_excel(file_name)
        headers = df_old.columns.tolist()
        df.columns = headers
        df_new = pd.concat([df_old, df])
        df_new.to_excel(file_name, index=False)

    # print("Data saved to book_td_data.xlsx")
