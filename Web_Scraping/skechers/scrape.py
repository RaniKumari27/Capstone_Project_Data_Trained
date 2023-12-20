import time
from pandas.core.dtypes.dtypes import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_data(url, driver):
    # url = "https://www.skechers.in/footsteps---transcend/111070-YEL.html"
    wait = WebDriverWait(driver, 5)
    driver.get(url)

    star = ""
    review_count = ""
    title = ""
    price = ""
    category = ""
    size = ""
    color_list = []
    product_code = ""
    data = []

    try:
        star_div = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".pr-snippet-rating-decimal"
        )))
        star = star_div.text
        review_div = wait.until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="pr-reviewsnippet"]/div/section/div/div[1]/div/div[2]/a[1]'
        )))
        review_count = re.findall(r'\d+', review_div.text)[0]
        title_div = driver.find_element(
            By.CSS_SELECTOR, ".product-name.hidden-sm-down")

        title = title_div.text
        price_div = wait.until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="maincontent"]/div[2]/div[3]/div[2]/div[5]/div/div/span/span[1]'
        )))
        price = price_div.text.replace(
            "₹", "").strip()
        category_div = driver.find_element(
            By.CSS_SELECTOR, ".pl-0.hidden-sm-down.product-gendername"
        )

        category = category_div.text.split("'")[0]
        size_div_parent = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="msq-histogram-sizing"]/div/div[2]/div[1]'
        )))

        size_div_list = size_div_parent.find_elements(By.TAG_NAME, "div")

        active_size_index = 0
        for size_div in size_div_list:
            if "pr-active" in str(size_div.get_attribute("class")):
                active_size_index = size_div_list.index(size_div) + 1

        size = active_size_index / 5 * 100

        color_list_parent = wait.until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="maincontent"]/div[2]/div[3]/div[2]/div[6]/div[2]/div/div'
        )))

        try:
            color_div_list = color_list_parent.find_elements(
                By.TAG_NAME, "button")

            for color_div in color_div_list:
                color = color_div.get_attribute("aria-describedby")
                color_list.append(color)
                color_div.click()
                time.sleep(1)
                product_code = driver.find_element(
                    By.XPATH, '//*[@id="maincontent"]/div[2]/div[3]/div[2]/div[6]/div[2]/div/div/div/div[2]/span[2]/span'
                ).text
                colors = [{f"color {i + 1}": color_list[i]} if
                          i < len(color_list) and len(color_list) > 1 else {
                    f"color {i + 1}": "None"}
                    for i in range(5)]
                size_count = ""
                try:
                    size_list_parent = wait.until(EC.presence_of_element_located((
                        By.XPATH, '//*[@id="size-0.0"]'
                    )))

                    raw_size_list = size_list_parent.find_elements(
                        By.TAG_NAME, "button")
                    size_list = []
                    for size_ele in raw_size_list:
                        if "disabled" not in str(size_ele.get_attribute("class")):
                            size_list.append(size_ele)
                    size_count = len(size_list)
                except Exception:
                    print("No size found")

                data_table = {
                    "shoe_name": title if title is not None else "NaN",
                    "price": price if price is not None else "NaN",
                    "url": url,
                    "category": category,
                    "review_count": review_count if review_count is not None else "NaN",
                    "star": star if star is not None else "NaN",
                    "product_code": product_code,
                    "shoe_type": "NaN",
                    "durability": "NaN",
                    "comfort": "NaN",
                    "size": size,
                    "size_count": size_count,
                    "color_count": len(color_list),
                    "brand": "skechers"
                }

                for _, color in enumerate(colors):
                    data_table.update(color)
                print(data_table)

                data.append(data_table)

        except Exception:
            color_list.append(url)

    except Exception:
        print("Some exception")
        pass
    return data
