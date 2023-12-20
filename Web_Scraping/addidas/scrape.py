import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def get_data(url, driver):
    driver.get(url)
    wait = WebDriverWait(driver, 5)

    title = ""
    original_price = ""
    discount_price = ""
    color_list = []
    product_code = []
    shoe_type = ""
    review_count = ""
    size = ""
    comfort = ""
    durability = ""
    url_list = []
    star_count = ""
    original_price = ""
    discount_price = ""
    data = []

    is_closed = False

    try:
        color_list_parent_div = None
        color_div_list = None
        color_url = None
        try:
            color_list_parent_div = WebDriverWait(driver, 2).until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="main-content"]/div[2]/div[2]/div[2]/div[2]'
            )))

            color_div_list = color_list_parent_div.find_elements(
                By.TAG_NAME, "a"
            )
            color_url = [color_div.get_attribute(
                "href") for color_div in color_div_list]
        except Exception:
            print("Price div not found")
        for i in range(len(color_div_list)):
            driver.get(str(color_url[i]))

            if is_closed is not True:
                try:
                    close_button = wait.until(EC.presence_of_element_located((
                        By.CLASS_NAME, "gl-modal__close"
                    )))

                    close_button.click()
                    is_closed = True
                except Exception:
                    is_closed = True
                    print("No close button found error")

            if is_closed:
                color_list_parent_div = wait.until(EC.presence_of_element_located((
                    By.XPATH, '//*[@id="main-content"]/div[2]/div[2]/div[2]/div[2]'
                )))

                color_div_list = color_list_parent_div.find_elements(
                    By.TAG_NAME, "a"
                )

                color_name = wait.until(EC.presence_of_element_located((
                    By.XPATH,
                    '//*[@id="main-content"]/div[2]/div[2]/div[2]/div[3]'
                ))).text
                url_list.append(driver.current_url)

                product_code.append(driver.current_url.split(
                    "/")[-1].replace(".html", ""))

                color_list.append(color_name)
                print("color found")
    except (TimeoutException, NoSuchElementException):
        color_div = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="main-content"]/div[2]/div[2]/div[2]'
        )))
        url_list.append(driver.current_url)

        product_code.append(driver.current_url.split(
            "/")[-1].replace(".html", ""))

        color_list.append(color_div.text)
        print("Color Exception")
    except Exception:
        print("Color exception")

    print(color_list,  url_list, product_code)

    try:
        title_div = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="main-content"]/div[2]/div[2]/div[1]/h1/span'
        )))
        title = title_div.text
        review_count = wait.until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="main-content"]/div[2]/div[2]/div[1]/div[1]/button'
        ))).text

        shoe_type_div = wait.until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="main-content"]/div[2]/div[2]/div[1]/div[1]/div/span'
        )))

        shoe_split = shoe_type_div.text.split("•")

        shoe_type = shoe_split
    except Exception:
        print("Static data error")

    review_parent_div = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR,
        '.accordion__header___3Pii5'
    )))

    try:
        review_button = wait.until(EC.presence_of_element_located((
            By.CLASS_NAME, 'accordion__header___3Pii5'
        )))

        review_button.click()

        star_count_div = wait.until(EC.presence_of_element_located((
            By.CLASS_NAME, 'rating___1z9bb'
        )))

        star_count = star_count_div.text
        slider_div_list = wait.until(EC.presence_of_all_elements_located((
            By.CLASS_NAME, "gl-comparison-bar__indicator"
        )))

        comfort_div = slider_div_list[0]
        durability_div = slider_div_list[1]
        size_div = slider_div_list[2]

        comfort = re.findall(
            f'\d+', str(comfort_div.get_attribute("style")))[0]
        durability = re.findall(
            f'\d+', str(durability_div.get_attribute("style")))[0]
        size = re.findall(f'\d+', str(size_div.get_attribute("style")))[0]
    except Exception:
        print("Dynamic data error")

    try:
        original_price_div = WebDriverWait(driver, 2).until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="main-content"]/div[2]/div[2]/div[1]/div[2]/div/div/div/div[1]'
        )))
        original_price = original_price_div.text.replace("₹", "")

        discount_price_div = WebDriverWait(driver, 2).until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="main-content"]/div[2]/div[2]/div[1]/div[2]/div/div/div/div[2]'
        )))

        discount_price = discount_price_div.text.replace("₹", "")
    except TimeoutException:
        try:

            original_price_div = WebDriverWait(driver, 2).until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="main-content"]/div[2]/div[2]/div[1]/div[2]/div/div/div/div'
            )))
            original_price = original_price_div.text.replace("₹", "")
            discount_price_div = "NaN"
            print("no discount")
        except TimeoutException:
            original_price_div = WebDriverWait(driver, 2).until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="main-content"]/div[2]/div[2]/div/div/div/div/div/div'
            )))
            original_price = original_price_div.text.replace("₹", "")
            discount_price_div = "NaN"
            print("Expensive shoe")
    except Exception:
        print("Unknown price error")

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
            "category": shoe_type[0] if len(shoe_type) > 1 else "Unisex",
            "review_count": review_count,
            "star": star_count,
            "product_code": product_code[i],
            "shoe_type": shoe_type[1] if len(shoe_type) > 1 else shoe_type[0] if len(shoe_type) != 0 else "Nan",
            "durability": durability,
            "comfort": comfort,
            "size": size,
            "size_count": "NaN",
            "color_count": len(color_list),
            "brand": "adidas"
        }
        for _, color in enumerate(colors):
            data_table.update(color)
        data.append(data_table)
    return data
