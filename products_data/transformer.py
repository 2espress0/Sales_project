# transformer.py 

import pandas as pd

class DataTransformer:
    def __init__(self, original_data):
        self.original_data = original_data

    def transform_data(self):
        # Remove rows with NaN values
        original_data = self.original_data.dropna()

        # Transform current_price column to float
        original_data['current_price'] = original_data['current_price'].str.replace(',', '').str.extract(r'(\d+\.\d+)').astype(float)

        # Transform avg_stars column to float
        original_data['avg_stars'] = original_data['avg_stars'].astype(float)

        # Transform num_reviews column to int
        original_data['num_reviews'] = original_data['num_reviews'].str.extract(r'(\d+)').astype(int)

        return original_data
