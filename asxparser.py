import csv
from bs4 import BeautifulSoup
from selenium import webdriver

def write_to_csv(rows, file_name): # writing data to csv file
    with open(file_name, "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)
        csv_file.close()

def snr_management_gender(person): # determining gender of senior management based off title, full name passed in as parameter
    switcher = {
        "Mr":"Male",
        "Ms":"Female"
    }
    return switcher.get(person[0:2], "ND")

def extract_data(table_row): # extracts data from a table row, converts it to text form, and returns data as a tuple
    table_header = table_row.find('th').text.strip()
    table_data = table_row.find('td').text.strip()
    return (table_header, table_data)

ASX_company = input("Enter an ASX listed company: ").upper()
url = "https://www.asx.com.au/asx/share-price-research/company/" + ASX_company + "/details"

driver = webdriver.Chrome()
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

company_detail_row_list = [[ASX_company + " Details"]]
company_people_row_list = [["Person", "Role", "Gender"]]

company_details = soup.find('table', attrs={'class':'table-people company-details'}) 
for table_row in company_details.find_all('tr', attrs={'class':''}):
    table_header, table_data = extract_data(table_row)
    csv_row = [table_header, table_data]
    company_detail_row_list.append(csv_row)

company_people = soup.find('table', attrs={'class':'table-people company-people'})
for table_row in company_people.find_all('tr'):
    table_header, table_data = extract_data(table_row)
    gender = snr_management_gender(table_header)
    csv_row = [table_header, table_data, gender]
    company_people_row_list.append(csv_row)

write_to_csv(company_detail_row_list, "Company Details - " + ASX_company + ".csv")
write_to_csv(company_people_row_list, "Company People - " + ASX_company + ".csv")