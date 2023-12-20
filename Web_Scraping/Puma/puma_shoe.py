from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def remove_words(s):
    pattern = re.compile(r'.*?(Women\'s|Men\'s|Unisex)\s*(.*)')
    match = re.match(pattern, s)
    if match:
        return match.group(2).strip()
    return s


def get_shoe(url, driver):
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    color_grid_div = wait.until(EC.presence_of_element_located(
        (
            By.CSS_SELECTOR, ".grid.gap-1"
        )))
    color_div_list = color_grid_div.find_elements(By.TAG_NAME, "label")

    data = []

    for color in color_div_list:
        shoe_info = {}

        color.click()
        time.sleep(1)

        title_h1 = wait.until(EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                ".tw-19nnhf.tw-lxvy65.tw-ou8532.tw-p9uz4a.tw-1h4nwdw"
            )))
        org_price_div = None
        discounted_price_div = None
        try:
            org_price_div = wait.until(EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '[data-test-id="item-sale-price-pdp"]'
                )))
            discounted_price_div = wait.until(EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '.whitespace-nowrap.text-base.line-through.opacity-50.override\\:font-bold.override\\:opacity-100'
                )))
        except TimeoutException:
            org_price_div = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id=item-price-pdp]"
            )))
            discounted_price_div = None
        except Exception:
            print("Error in price")

        size_div_list = wait.until(EC.presence_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                ".relative.border.flex.items-center.justify-center.flex-none.rounded-sm.cursor-pointer"
            )))
        product_code_parent_div = wait.until(EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                ".tw-1h4nwdw.tw-p9uz4a.tw-xwzea6.list-disc.list-inside"
            )))

        product_code_div = product_code_parent_div.find_element(
            By.TAG_NAME, "li"
        )
        category = "Men" if "Men" in title_h1.text else "Women" if "Women" in title_h1.text else "Unisex"
        color_list = []
        for color_k in color_div_list:
            color_text = color_k.find_element(By.CLASS_NAME, "sr-only").text
            color_list.append(color_text)

        colors = [{f"color {i + 1}": color_list[i]} if
                  i < len(color_list) and len(color_list) > 1 else {
                      f"color {i + 1}": "None"}
                  for i in range(5)]

        shoe_info['shoe_name'] = title_h1.text
        shoe_info['org_price'] = org_price_div.text
        shoe_info['discounted_price'] = discounted_price_div.text if discounted_price_div is not None else "NaN"
        shoe_info['url'] = url
        shoe_info['category'] = category
        shoe_info['review_count'] = "None"
        shoe_info['star'] = "None"
        shoe_info['product_code'] = product_code_div.text.replace(
            "Style:", "").strip()
        shoe_info['shoe_type'] = remove_words(title_h1.text)
        shoe_info['durability'] = "None"
        shoe_info['comfort'] = "None"
        shoe_info['size'] = "None"
        shoe_info['size_count'] = len(size_div_list)
        shoe_info['color_count'] = len(color_div_list)
        shoe_info["brand"] = "Puma"

        data_table = {
            'shoe_name': shoe_info['shoe_name'],
            'org_price': shoe_info['org_price'],
            'discounted_price': shoe_info['discounted_price'],
            'url': shoe_info['url'],
            'category': shoe_info['category'],
            'review_count': shoe_info['review_count'],
            'star': shoe_info['star'],
            'product_code': shoe_info['product_code'],
            'shoe_type': shoe_info['shoe_type'],
            'durability': shoe_info['durability'],
            'comfort': shoe_info['comfort'],
            'size': shoe_info['size'],
            'size_count': shoe_info['size_count'],
            'color_count': shoe_info['color_count'],
            'brand': shoe_info['brand'],
        }

        for _, color in enumerate(colors):
            data_table.update(color)

        print(data_table)
        data.append(data_table)
    return data
