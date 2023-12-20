from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re


def save_to_csv(shoe_data):
    try:
        existing_csv = pd.read_csv("puma-link.csv")
    except Exception:
        existing_csv = pd.DataFrame()

    shoe_df = pd.DataFrame(shoe_data)
    df = pd.concat([existing_csv, shoe_df], ignore_index=True)

    df.to_csv("puma-link.csv", index=False)

    print("CSV file './puma-link.csv' saved successfully.")


def get_links():

    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    shoe_urls = []

    for url in urls:
        driver.get(url)
        item_count_div = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".uppercase.font-bold.text-lg.md\\:text-xl"
        )))

        item_count = int(re.findall("\d+", item_count_div.text)[0])

        print(item_count)
        i = 0
        while i < item_count:
            try:
                url_parent_div_list = wait.until(EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR, "a[data-test-id=product-list-item-link]"
                )))

                driver.execute_script(
                    "arguments[0].scrollIntoView(true);", url_parent_div_list[-1])

                if i > 0:
                    url_parent_div_list = url_parent_div_list[i:]

                url_element = url_parent_div_list[0]
                shoe_url = url_element.get_attribute("href")

                shoe_urls.append({"link": shoe_url})
                i += 1

                print(
                    f"length of shoe urls for loop {i} is {len(shoe_urls)}")
                print(f"url for this loop is {shoe_url}")
                data = {"link": shoe_url}
                save_to_csv([data])
            except Exception as e:
                print(f"Error: {e}")
                print("Not loaded yet")

        df = pd.DataFrame(shoe_urls)
        df.to_csv("./puma-link.csv", index=False)

    driver.quit()


urls = ["https://in.puma.com/in/en/womens/womens-shoes"]

get_links()
