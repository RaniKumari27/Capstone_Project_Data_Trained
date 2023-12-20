from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup

# Creates Chrome WebDriver instance.
driver = webdriver.Chrome()
driver.maximize_window()

# Navigate to shine website
driver.get("https://www.skechers.in/men/footwear?start=0&sz=24")

# Wait for the page to load
time.sleep(3)

# Close the pop-up dialog (if it appears)
try:
    x = driver.find_element(
        By.XPATH, '//*[@id="consent-tracking"]/div/div/div[2]/div[2]/div/button[2]')
    x.click()
except NoSuchElementException:
    pass
time.sleep(10)

data = []

while True:
    # Imports the HTML of the webpage into python
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # grabs the HTML of each product
    product_card = soup.find_all('div', class_='tile-name-price pt-2')

    # Grabs the product details for every product on the page and adds each product as a row in our dataframe
    for product in product_card:
        try:
            link = product.find('a', class_='link p-heading').get('href')
            data.append({"Link": link})
        except Exception:
            pass

    # Find and click the next page link
    next_page = soup.find('a', class_="page-link next")

    if next_page:
        next_page_url = next_page.get('href')
        driver.get(next_page_url)
        time.sleep(5)  # Add a sleep to allow the page to load
    else:
        break

# Create a DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv("skechers_links_data_men.csv", index=False)

# Close the Chrome WebDriver
driver.quit()
