import pandas as pd
from selenium import webdriver
from pandas.errors import EmptyDataError
from scrape import get_data

# import all the links from skechers-link
df = pd.read_csv('./skechers-link.csv')

# get all links
links = df['link']

options = webdriver.ChromeOptions()


def setup_driver():
    return webdriver.Chrome(options=options)


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


# Loop through links
for link in links:
    print(link)

    # Initialize a new WebDriver for each URL
    driver = setup_driver()
    driver.maximize_window()

    data_list_for_link = get_data(link, driver)
    save_data_to_csv(data_list_for_link)

    # Quit the WebDriver after processing each URL
    driver.quit()
