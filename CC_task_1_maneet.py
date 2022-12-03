# Python Program for Myntra Web Scrapping

# Imports
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from config import *

driver = webdriver.Chrome(ChromeDriverManager().install())
# driver = webdriver.Chrome()


def main(page, search):
    product_rating = []
    product_brand = []
    product = []
    driver.get(f"{PRODUCT_SITE}{search}?p={page}")
    content = driver.page_source
    soup = BeautifulSoup(content)
    for item in soup.findAll('li', attrs={'class': 'product-base'}):
        metadata_div = item.find(
            'div', attrs={'class': 'product-productMetaInfo'})
        pname = metadata_div.find(
            'h4', attrs={'class': 'product-product'}).text

        if PRODUCT_NAME_FILTER not in pname:
            continue

        brand = metadata_div.find('h3', attrs={'class': 'product-brand'}).text

        try:
            rating_div = item.find(
                'div', attrs={'class': 'product-ratingsContainer'})
            rating = rating_div.find('span', attrs={}).text
        except:
            rating = "NA"

        product_brand.append(brand)
        product.append(pname)
        product_rating.append(rating)
    return product_brand, product, product_rating



def to_csv(product_brand, product, product_rating):
    df = pd.DataFrame({'Product Name': product,
                      'Product Brand': product_brand, 'Product Rating': product_rating})
    df.head()
    df.to_csv(CSV_FILE_NAME, index=False, encoding='utf-8')


if __name__ == "__main__":
    final_product_brand = []
    final_product = []
    final_product_rating = []
    pages = DEFAULT_PAGES
    search = SEARCH_TEXT
    for page in range(1, pages+1):
        product_brand, product, product_rating = main(
            page, search)
        final_product_brand.extend(product_brand)
        final_product.extend(product)
        final_product_rating.extend(product_rating)

    to_csv(final_product_brand, final_product, final_product_rating)

   