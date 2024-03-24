from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd

driver = webdriver.Chrome()

driver.get("https://en.hygieneblackspots.gov.hk/hygiene-black-spots-en/page/districts")

# Need a wait before find elements, because the webpage is loaded first, but data comes later.
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a.markuid___app_project_modules_document-collection_document_document-element_hyperlink-element_a_15c654"))
)

a_tag_to_districts = driver.find_elements(By.CSS_SELECTOR, "a.markuid___app_project_modules_document-collection_document_document-element_hyperlink-element_a_15c654")

# Extract the url from a-tags, and store the string only
# DO NOT STORE THE A-TAGS: Once the page is reloaded, or navigated away, these a-tags become staled element
# When you click on a staled element, selenium will throw error

urls = [(tag.text, tag.get_attribute('href')) for tag in a_tag_to_districts]

result = []

for district_name, url in urls:

    print("Processing:", district_name)

    driver.get(url)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h3.text-header"))
    )
    title_tags = driver.find_elements(By.CSS_SELECTOR,"h3.text-header")

    titles = [title_tag.text for title_tag in title_tags]

    extraction_regex = r'([A-Z]{2}-\d{6})\s(.*)\s\(([^()]*)\)'

    for title in titles:
        re_result = re.search(extraction_regex, title)

        result.append([district_name, re_result.group(1), re_result.group(2), re_result.group(3)])

driver.close()

result_df = pd.DataFrame(result, columns=["District name", "Code", "Location", "Problem"])

result_df.set_index(["Code"]).sort_index().to_csv("data_from_selenium.csv")
