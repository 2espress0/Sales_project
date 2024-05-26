import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from config import CATEGORY_URLS

class JumiaScraper:
    def __init__(self):
        pass
    
    def get_pagination_count(self, category_url):
        response = requests.get(category_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            pagination_links = soup.find_all("a", class_="pg")
            if pagination_links:
                last_page_link = pagination_links[-1].get("href")
                last_page_number = int(last_page_link.split("=")[-1].split("#")[0])
                return last_page_number
            else:
                return 1
        else:
            print(f"Failed to retrieve the page: {category_url}", flush=True)
            return 0
    
    def construct_page_url(self, category_url, page_number):
        return f"{category_url}&page={page_number}"
    
    def scrape_category(self):
        all_categories_data = []
        for category_url in CATEGORY_URLS:
            print(f"Accessing the category page: {category_url}...", flush=True)
            category_data = self.scrape_category_url(category_url)
            all_categories_data.append(category_data)
        return pd.concat(all_categories_data, ignore_index=True)

    def scrape_category_url(self, category_url):
        pagination_count = self.get_pagination_count(category_url)
        if pagination_count == 0:
            print(f"Skipping category: {category_url}", flush=True)
            return pd.DataFrame()

        print(f"Found {pagination_count} pages of products for {category_url}.", flush=True)

        category_name = category_url.split('/')[-2]
        category_products_data = []
        for page_number in range(1, pagination_count + 1):
            print(f"Accessing page {page_number}...", flush=True)
            page_data = self.scrape_category_page(category_url, page_number, category_name)
            num_products = len(page_data)
            category_products_data.append(page_data)
            print(f"Found {num_products} products on page {page_number}.", flush=True)

        print(f"All pages scraped for category {category_url}.", flush=True)
        return pd.concat(category_products_data, ignore_index=True)

    def scrape_category_page(self, category_url, page_number, category_name):
        url = self.construct_page_url(category_url, page_number)
        response = requests.get(url)
        if response.status_code == 200:
            time.sleep(2)
            soup = BeautifulSoup(response.content, "html.parser")
            product_elements = soup.find_all("article", class_="prd _fb col c-prd")
            products_data = []
            for product_element in product_elements:
                product_link = product_element.find("a", class_="core")["href"]
                product_link = f"https://www.jumia.ma{product_link}"
                product_name = product_element.find("h3", class_="name").text.strip()
                current_price = product_element.find("div", class_="prc").text.strip()
                avg_stars = product_element.find("div", class_="rev").text.strip().split()[0]
                num_reviews = product_element.find("div", class_="rev").text.strip().split()[-1][1:-1]
                product_data = {
                    "category": category_name,
                    "link": product_link,
                    "name": product_name,
                    "current_price": current_price,
                    "avg_stars": avg_stars,
                    "num_reviews": num_reviews
                }
                products_data.append(product_data)
            return pd.DataFrame(products_data)
        else:
            print(f"Failed to retrieve page {page_number} for category: {category_url}", flush=True)
            return pd.DataFrame()
