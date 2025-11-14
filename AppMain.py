import os
import pandas as pd

class AppMain:
    def __init__(self):
        self.path = os.getcwd()
        self.ingredients_file = "Ingredients.csv"
        self.products_file = "Products.csv"

    def get_ingredients_df(self):
        df = pd.read_csv(f"{self.path}/{self.ingredients_file}")
        return df

    def update_ingredients_file(self, data):
        df = pd.DataFrame(data)
        df.to_csv(f"{self.path}/{self.ingredients_file}", index=False)

if __name__ == "__main__":
    main = AppMain()