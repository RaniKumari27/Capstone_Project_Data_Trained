from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

men_links = [
    "https://www.woodlandworldwide.com/product-list/MEN_BOOTS",
    "https://www.woodlandworldwide.com/product-list/MEN_SNEAKERS",
    "https://www.woodlandworldwide.com/product-list/MEN_CASUALS_LACE_UP",
    "https://www.woodlandworldwide.com/product-list/MEN_CASUALS_SLIP_ON",
    "https://www.woodlandworldwide.com/product-list/MEN_CANVAS",
    "https://www.woodlandworldwide.com/product-list/MEN_FORMAL_SLIP_ON",
    "https://www.woodlandworldwide.com/product-list/MEN_FORMAL_LACE_UP",
    "https://www.woodlandworldwide.com/product-list/MEN_SLIPPERS",
    "https://www.woodlandworldwide.com/product-list/MENS_CASUAL_SANDALS",
    "https://www.woodlandworldwide.com/product-list/MEN_SPORTS_SANDALS"
]


def get_links(urls):
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 5)
    shoe_urls = []

    for url in urls:
        driver.get(url)
        item_count_div = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            '.MuiTypography-root.MuiTypography-body1.css-1s2byso'
        )))

        print(item_count_div.text.split(" "))

        item_count = item_count_div.text.split(" ")[6]
        i = 0
        while i < int(item_count):
            # Scroll to the end of the page.
            url_parent_div_list = wait.until(EC.presence_of_all_elements_located((
                By.CLASS_NAME, "productcardplp_productwrapper__x83B9",
            )))
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", url_parent_div_list[-1])

            if i > 0:
                url_parent_div_list = url_parent_div_list[i:]

            if len(url_parent_div_list) != 0:
                url_element = url_parent_div_list[0].find_element(
                    By.TAG_NAME, "a")

                url = url_element.get_attribute('href')
                print(url)

                shoe_urls.append(url)
                i += 1

    driver.quit()
    df = pd.DataFrame(shoe_urls)
    df.to_csv("./nike-link.csv", index=False)


get_links(men_links)
