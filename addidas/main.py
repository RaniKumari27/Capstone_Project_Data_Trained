import pandas as pd
from pandas.errors import EmptyDataError
from selenium import webdriver
from scrape import get_data

# import all the links from adidas-link
df = pd.read_csv('./adidas-link.csv')

# get all links
links = df['link']

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
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

    # Concat
    df = pd.concat([existing_csv, shoe_df], ignore_index=True)
    # Save the DataFrame to a CSV file
    df.to_csv(csv_filename, index=False)

    print(f"CSV file '{csv_filename}' saved successfully.")


data_list = []

for link in links:
    print(link)
    data_list_for_link = get_data(link, driver)
    data_list.append(data_list_for_link)
    save_data_to_csv(data_list_for_link)

df_1 = pd.DataFrame(data_list)

# Save the DataFrame to a CSV file
save_data_to_csv(data_list)

driver.quit()
