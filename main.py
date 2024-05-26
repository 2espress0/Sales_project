import os
import pandas as pd
from products_data.scraper import JumiaScraper
from products_data.transformer import DataTransformer
from config import CATEGORY_URLS

def main():
    # Specify the folder path to save CSV files
    datasets_folder = os.path.join(os.getcwd(), 'datasets')

    # Initialize JumiaScraper object for products_sold_data
    jumia_scraper = JumiaScraper()
    sold_data = jumia_scraper.scrape_category()
    
    # Initialize DataTransformer object for products_sold_data
    transformer = DataTransformer(sold_data)
    transformed_sold_data = transformer.transform_data()

    # Save transformed_sold_data to CSV in the datasets folder
    sold_file_path = os.path.join(datasets_folder, 'products_sold_data.csv')
    transformed_sold_data.to_csv(sold_file_path, index=False)
    print(f"Sold products data saved to {sold_file_path}", flush=True)


if __name__ == "__main__":
    main()