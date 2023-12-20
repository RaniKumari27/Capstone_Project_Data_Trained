import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def extract_fit_information(input_string,):
    fits = re.findall(r'(Fits\s+)(large|medium|regular)', input_string)
    return fits


def scrape(url, driver):
    wait = WebDriverWait(driver, 5)
    driver.get(url)

    color_div_parent = None
    color_div_list = []

    data = []

    try:
        color_div_parent = driver.find_element(
            By.CSS_SELECTOR, ".colorway-images.ta-sm-c.d-lg-t"
        )

        color_div_list = color_div_parent.find_elements(
            By.CSS_SELECTOR,
            ".css-7aigzk.colorway-container.d-sm-ib.d-lg-tc.pr1-sm.pb1-sm")
    except NoSuchElementException:
        print("No colors")
        color_div_list.append(url)

    comfort = ""
    fit = ""
    review_count = 0
    try:
        review_count_div = wait.until(EC.presence_of_all_elements_located((
            By.CLASS_NAME, "css-rptnlm"
        )))[0]

        review_count = re.findall(
            "\d+", review_count_div.find_element(By.TAG_NAME, "h3").text)[0]

        more_review_button = None
        review_button = None

        try:
            review_button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "summary.css-rptnlm"
            )))

            review_button.click()

            more_review_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, "button[data-test=more-reviews]"
            )))

            driver.execute_script(
                "arguments[0].scrollIntoView(true);", more_review_button)
        except TimeoutException or NoSuchElementException:
            print("More button not found")
            pass

        if more_review_button is not None:
            try:
                more_review_button.click()

                time.sleep(1)

                slider_divs = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((
                    By.CLASS_NAME, "tt-u-clip-hide"
                )))
                comfort_div = slider_divs[1]
                comfort = re.findall(
                    "\d+", comfort_div.text)[0] if comfort_div is not None else "None"
                fit_div = slider_divs[0]
                fit = re.findall(
                    "\d+", fit_div.text)[0] if fit_div is not None else "None"
                close_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    ".css-7vvfsw.css-1v3caum.js-drawer-close.g72-x.bg-white.z10"
                )))
                close_button.click()

            except Exception:
                close_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    ".css-7vvfsw.css-1v3caum.js-drawer-close.g72-x.bg-white.z10"
                )))
                close_button.click()
                comfort = "None"
                fit = "None"
    except Exception:
        print("Review not found")
        pass

    for color_div in color_div_list:
        if color_div_parent is not None:
            driver.execute_script(
                "window.scrollTo(0, 0);")
            color_div.click()

        try:
            color_div_parent = driver.find_element(
                By.CSS_SELECTOR, ".colorway-images.ta-sm-c.d-lg-t"
            )

            color_div_list = color_div_parent.find_elements(
                By.CSS_SELECTOR,
                ".css-7aigzk.colorway-container.d-sm-ib.d-lg-tc.pr1-sm.pb1-sm")
        except Exception:
            pass

        title_div = wait.until(EC.presence_of_all_elements_located((
            By.CSS_SELECTOR, ".headline-2.css-16cqcdq"
        )))[1]

        price_div = None

        try:
            price_div = wait.until(EC.presence_of_all_elements_located((
                By.CSS_SELECTOR,
                ".product-price.css-11s12ax.is--current-price.css-tpaepq"
            )))[1]
        except Exception:
            price_div_parent = wait.until(EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, ".product-price__wrapper.css-13hq5b3"
            )))[1]
            price_div = price_div_parent.find_element(
                By.TAG_NAME,
                "div"
            )
        except:
            print("Couldn't get price;")
            pass

        shoe_type_div = wait.until(EC.presence_of_all_elements_located((
            By.CSS_SELECTOR, ".headline-5.pb1-sm.d-sm-ib"
        )))[1]

        # shoe_type_div = shoe_type_div_parent.find_element(By.TAG_NAME, "h2")

        print(shoe_type_div.text)

        size_div_parent = None
        size_div_list = []
        try:
            size_div_parent = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, ".mt5-sm.mb3-sm.body-2.css-1pj6y87"
            )))
            size_div = size_div_parent.find_element(
                By.CSS_SELECTOR, ".mt2-sm.css-12whm6j"
            )
            size_div_list = size_div.find_elements(By.TAG_NAME, "div")
        except Exception:
            print("Error")
            pass

        star_div = None
        try:
            review_parent_div = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, ".css-rptnlm",
            )))

            star_div = review_parent_div.find_element(
                By.CLASS_NAME, "css-n209rx"
            )  # attr = aria-label
        except Exception:
            pass

        category_div = wait.until(EC.presence_of_all_elements_located((
            By.CSS_SELECTOR, ".headline-5.pb1-sm.d-sm-ib"
        )))[1]

        product_code_div = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".description-preview__style-color.ncss-li"
        )))

        colors = [{f"color {i + 1}": color_div_list[i].find_element(By.TAG_NAME, 'img').get_attribute("alt")} if
                  i < len(color_div_list) and len(color_div_list) > 1 else {
                      f"color {i + 1}": "None"}
                  for i in range(5)]
        category = "Men" if "Men" in category_div.text else "Women" if "Women" in category_div.text else "Unisex"

        # Fit and comfort div

        comfort_div = None
        fit_div = None

        time.sleep(2)

        # Scroll to the element

        # slider_div_list = wait.until(EC.presence_of_all_elements_located((
        #     By.CSS_SELECTOR, ".tt-c-summary-dim-range__dot"
        # )))

        data_table = {
            "shoe_name": title_div.text.strip(),
            "price": price_div.text.split("₹")[1].strip() if price_div
            is not None else "None",
            "url": url,
            "category": category,
            "review_count": review_count,
            "star": str(star_div.get_attribute(
                'aria-label')).strip() if star_div is not None else "NaN",
            "product_code": product_code_div.text.replace(
                "Style: ", "").strip(),
            "shoe_type": shoe_type_div.text.replace(category +
                                                    "'s", "").strip() if shoe_type_div is not None else "NaN",
            "durability": "None",
            "comfort": comfort if comfort is not None else "NaN",
            "size": fit if fit is not None else "NaN",
            "size_count": len(size_div_list),
            "color_count": len(color_div_list),
            "brand": "Nike",
            # "sizes": [size.text for size in size_div_list]
        }
        for _, color in enumerate(colors):
            data_table.update(color)

        print(data_table)

        data.append(data_table)

    return data
