from pandas.core.dtypes.dtypes import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd


def get_links():

    driver = webdriver.Chrome()

    driver.maximize_window()

    urls = ["https://columbiasportswear.co.in/women/footwear-women",
            "https://columbiasportswear.co.in/men/footwear-men"]

    shoe_urls = []
    for url in urls:
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        total_item_div = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "category-total-item")))

        total_item = int(re.findall("\d+", total_item_div.text)[0])

        print(total_item)

        for i in range(total_item):

            # Scroll to the end of the page.
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # sleep(1)

            url_parent_div_list = wait.until(EC.presence_of_all_elements_located((
                By.CSS_SELECTOR,
                ".product-layout.product-item.product-grid.col-xs-6.col-md-4.col-lg-3"
            )))

            if i > 0:
                url_parent_div_list = url_parent_div_list[i:]

            url_parent_div = url_parent_div_list[0]

            url_element = url_parent_div.find_element(By.TAG_NAME, "a")

            shoe_urls.append({"link": url_element.get_attribute("href")})
            # print(url_element.get_attribute("href"))

    df = pd.DataFrame(shoe_urls)
    df.to_csv("./columbia-link.csv", index=False)


get_links()
