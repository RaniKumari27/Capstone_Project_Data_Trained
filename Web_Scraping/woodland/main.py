import pandas as pd
from selenium import webdriver
from pandas.errors import EmptyDataError
from scrape_wood import get_data

# import all the links from puma-link
df = pd.read_csv('./woodland-link.csv')

# get all links
links = df['link']

driver = webdriver.Chrome()
driver.maximize_window()


def save_data_to_csv(data_list, csv_filename='output.csv'):
    shoe_data = []
    for data in data_list:
        shoe_data.append(data)
        print(data)
        print("\n")
    shoe_df = pd.DataFrame(shoe_data)

    try:
        existing_csv = pd.read_csv(csv_filename)
    except EmptyDataError:
        existing_csv = pd.DataFrame()

    # Save the DataFrame to a CSV file
    df = pd.concat([existing_csv, shoe_df], ignore_index=True)
    # Save the DataFrame to a CSV file
    df.to_csv(csv_filename, index=False)

    print(f"CSV file '{csv_filename}' saved successfully.")


for link in links:
    print(link)
    data_list_for_link = get_data(link, driver)
    save_data_to_csv(data_list_for_link)


driver.quit()
