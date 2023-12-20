import pandas as pd
from selenium import webdriver
from pandas.errors import EmptyDataError
from puma_shoe import get_shoe

# import all the links from puma-link
df = pd.read_csv('./puma-link.csv')

# get all links
links = df['link']

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.maximize_window()


def save_data_to_csv(data_list, csv_filename='output.csv'):
    shoe_data = []
    for data in data_list:
        shoe_data.append(data)
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


data_list = []

for link in links:
    print(link)
    data_list_for_link = get_shoe(link, driver)
    save_data_to_csv(data_list_for_link)


driver.quit()
