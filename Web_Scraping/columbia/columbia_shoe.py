from pandas.core.dtypes.dtypes import re
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import os


def get_columbia_shoe(url, driver):

    driver.get(url)

    color_list_div = []
    color_urls = []
    color_list = []
    shoe_info_list = []

    try:
        color_list_div = driver.find_element(
            By.CLASS_NAME, "grop-product-product")
        color_list = color_list_div.find_elements(By.TAG_NAME, "a")

        for color_div in color_list:
            url = color_div.get_attribute("href")
            color_urls.append(url)
    except NoSuchElementException:
        print("No colors")
        color_urls.append(url)

    for i in range(len(color_urls)):
        shoe_info = {
            "color_name": any,
            "product_info": {}
        }
        if len(color_urls) > 1:
            try:
                if len(color_list) > 1:
                    shoe_info = {
                        "color_name": color_list[i].get_attribute('data-color'),
                        "product_info": {}
                    }

            except StaleElementReferenceException:
                pass

        driver.get(color_urls[i])
        try:
            color_list_div = driver.find_element(
                By.CLASS_NAME, "grop-product-product")
            color_list = color_list_div.find_elements(By.TAG_NAME, "a")
        except NoSuchElementException:
            print("No colors")

        wait = WebDriverWait(driver, 10)

        title_div = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "product-title")))

        price_parent = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".list-unstyled.price-container"
        )))

        print(len(price_parent.find_elements(By.TAG_NAME, "li")))

        try:
            dis_price_div = price_parent.find_elements(
                By.TAG_NAME, "li")[1]
        except IndexError:
            dis_price_div = None

        org_price_div = price_parent.find_elements(By.TAG_NAME,
                                                   "li")[0]

        size_div_list = []
        try:

            size_div_parent = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "option-main")))
            size_div_list = size_div_parent.find_elements(By.CSS_SELECTOR,
                                                          "div.radio.radio-type-button2  ")
        except Exception:
            pass
        review_div = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "review_total")))
        star_count_div = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "actual-star")))
        data_col_div = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "col-sm-5")))
        product_code_div = data_col_div.find_element(By.TAG_NAME, "p")
        category = "Men" if "Men" in title_div.text else "Women" if "Women" in title_div.text else "Unisex"

        shoe_info["product_info"]["title"] = title_div.text
        shoe_info["product_info"]["dis_price"] = "NaN" if dis_price_div is None else dis_price_div.text
        shoe_info["product_info"]["org_price"] = org_price_div.text
        shoe_info["product_info"]["size"] = [re.findall("UK-\d+", i.text.strip())[0]
                                             for i in size_div_list]
        shoe_info["product_info"]["star_count"] = star_count_div.text[0]
        shoe_info["product_info"]["product_code"] = product_code_div.text.replace(
            "SKU :", "").strip()
        shoe_info['product_info']["category"] = category
        shoe_info['product_info']["review_count"] = review_div.text

        shoe_info_list.append(shoe_info)

    data_list = []
    data_table = {}
    for shoe_info in shoe_info_list:
        product_info = shoe_info['product_info']

        colors = [{f"color {i + 1}": color_list[i].get_attribute('data-color')} if
                  i < len(color_list) else {f"color {i + 1}": "NaN"}
                  for i in range(5)]

        data_table = {
            "shoe_name": product_info['title'],
            "original_price": product_info['org_price'],
            "discounted_price": product_info['dis_price'],
            "url": url,
            "category": product_info['category'],
            "review_count": product_info['review_count'],
            "star": product_info['star_count'],
            "product_code": product_info['product_code'],
            "shoe_type": "NaN",
            "durability": "NaN",
            "comfort": "NaN",
            "size": "NaN",
            "size_count": len(product_info['size']),
            "color_count": len(color_list),
            "brand": "columbia",
        }
        for i, color in enumerate(colors):
            data_table.update(color)
        data_list.append(data_table)

    color_list_div = []
    color_urls = [url]
    color_list = []
    shoe_info_list = []

    return data_list
