import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_data(url, driver):
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    title = ""
    original_price = ""
    discount_price = ""
    color_list = []
    product_code = []
    size_count = []
    url_list = []
    data = []

    color_list_parent_div = wait.until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="__next"]/div[2]/div/div[1]/div[2]/div[2]/div/div[2]'
    )))

    color_div_list = color_list_parent_div.find_elements(
        By.CSS_SELECTOR, ".colorpicker_option__B8oxU"
    )

    for i in range(len(color_div_list)):
        color_div_list[i].click()
        time.sleep(1)

        color_list_parent_div = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="__next"]/div[2]/div/div[1]/div[2]/div[2]/div/div[2]'
        )))

        color_div_list = color_list_parent_div.find_elements(
            By.CSS_SELECTOR, ".colorpicker_option__B8oxU"
        )

        color_name = wait.until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="__next"]/div[2]/div/div[1]/div[2]/div[2]/div/div[1]/h5'
        ))).text
        url_list.append(driver.current_url)

        product_code.append(driver.current_url.split("/")[-1])

        size_parent_div = wait.until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="__next"]/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div'
        )))

        size_button_list = size_parent_div.find_elements(
            By.TAG_NAME, "button"
        )

        size_list = []

        for i in range(len(size_button_list)):
            if size_button_list[i].get_attribute("disabled") != "true":
                size_list.append(size_button_list[i])
        size_count.append(len(size_list))

        color_list.append(color_name)

    try:
        title_div = wait.until(EC.presence_of_element_located((
            By.CLASS_NAME, "productprice_productname__7Lzg5"
        )))
        title = title_div.text.strip()

        original_price_div = wait.until(EC.presence_of_element_located((
            By.CLASS_NAME, "productprice_offerprice__RLPOw"
        )))

        original_price = original_price_div.text.replace("₹", "").strip()

        discount_price_parent_div = wait.until(EC.presence_of_element_located((
            By.CLASS_NAME, "productprice_mrpprice__7zMlK"
        )))
        discount_price_div = discount_price_parent_div.find_element(
            By.TAG_NAME, "span")
        discount_price = discount_price_div.text.replace(
            "₹", "").strip()

    except Exception as e:
        print(f"General data error: {e}")

    for i in range(len(color_list)):

        colors = [{f"color {i + 1}": color_list[i]} if
                  i < len(color_list) and len(color_list) > 1 else {
                      f"color {i + 1}": "None"}
                  for i in range(5)]
        data_table = {
            "shoe_name": title,
            "original_price": original_price,
            "discount_price": discount_price,
            "url": url_list[i],
            "category": "Men",
            "review_count": "Nan",
            "star": "Nan",
            "product_code": product_code[i],
            "shoe_type": title.split("for")[0].split(
                "For")[0].strip().split(" ")[-1],
            "durability": "Nan",
            "comfort": "Nan",
            "size": "size",
            "size_count": size_count[i],
            "color_count": len(color_list),
            "brand": "Woodland"
        }
        for _, color in enumerate(colors):
            data_table.update(color)
        data.append(data_table)

    return data
