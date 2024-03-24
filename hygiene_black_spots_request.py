import requests
import pandas as pd
import re

url_menu_item = "https://en.hygieneblackspots.gov.hk/api/NavMenu/GetNavMenuContent"
response = requests.get(url_menu_item, headers={"Project-Code": "hygiene-black-spots-en"})

district_nav_items = response.json()['navMenuGroups'][3]['navMenuItems'][1:]

district_info = []

for nav_item in district_nav_items:
    district_info.append([nav_item['name'], nav_item['childPanelDocumentCollectionId']])

result = []

for district_name, district_id in district_info:

    print("Processing:", district_name)

    url = f"https://en.hygieneblackspots.gov.hk/api/DocumentCollections/GetDocumentCollection?id={district_id}"

    response = requests.get(url, headers={"Project-Code": "hygiene-black-spots-en"})
    document_elements = response.json()['documents'][1]['documentElements']

    for element in document_elements:
        name = element.get('name', None)

        if name is not None and len(name) > 0:

            extraction_regex = r'([A-Z]{2}-\d{6})\s(.*)\s\(([^()]*)\)'

            re_result = re.search(extraction_regex, name)

            result.append([district_name, re_result.group(1), re_result.group(2), re_result.group(3)])

result_df = pd.DataFrame(result, columns=["District name", "Code", "Location", "Problem"])

result_df.set_index(["Code"]).sort_index().to_csv("data_from_request.csv")
