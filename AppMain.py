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
        df = df.sort_values(by="Ingredient")
        df.to_csv(f"{self.path}/{self.ingredients_file}", index=False)

    def get_products_list(self):
        df = pd.read_csv(f"{self.path}/{self.products_file}")
        product_list = df["Product"].values.tolist()
        return product_list

    def get_ingredient_list(self):
        df = pd.read_csv(f"{self.path}/{self.ingredients_file}")
        ingredient_list = df["Ingredient"].values.tolist()
        return ingredient_list

    def get_ingredient_cost(self, ingredient_name, ingredient_unit):
        df = pd.read_csv(f"{self.path}/{self.ingredients_file}")

        ingredient_row = None
        for i, row in df.iterrows():
            if row["Ingredient"] == ingredient_name:
                density = df.at[i, "Density (g/ml)"]
                price = df.at[i, "Store Price (€)"]
                amount = df.at[i, "Store Amount"]
                unit = df.at[i, "Store Unit"]
                ingredient_row = row
                break

        if ingredient_row is None:
            return None

        price_per_g = None
        price_per_ml = None
        price_per_pc = None

        if unit == "g":
            price_per_g = price / amount
            price_per_ml = price / amount * density
        elif unit == "kg":
            price_per_g = price / amount / 1E3
            price_per_ml = price / amount / 1E3 * density
        elif unit == "ml":
            price_per_g = price / amount / density if density > 0 else None
            price_per_ml = price / amount
        elif unit == "l":
            price_per_g = price / amount / 1E3 / density if density > 0 else None
            price_per_ml = price / amount / 1E3
        elif unit == "lb":
            price_per_g = price / amount / 453.592
            price_per_ml = price / amount / 453.592 * density
        elif unit == "oz":
            price_per_g = price / amount / 28.3495
            price_per_ml = price / amount / 28.3495 * density
        elif unit == "pc":
            price_per_pc = price / amount
        else:
            return None

        if ingredient_unit == "g":
            cost = price_per_g
        elif ingredient_unit == "kg":
            cost = price_per_g * 1E3 if price_per_g else None
        elif ingredient_unit == "lb":
            cost = price_per_g * 453.592 if price_per_g else None
        elif ingredient_unit == "oz":
            cost = price_per_g * 28.3495 if price_per_g else None
        elif ingredient_unit == "ml":
            cost = price_per_ml
        elif ingredient_unit == "l":
            cost = price_per_ml * 1E3 if price_per_ml else None
        elif ingredient_unit == "cup":
            cost = price_per_ml * 236.588 if price_per_ml else None
        elif ingredient_unit == "tsp":
            cost = price_per_ml * 4.92892 if price_per_ml else None
        elif ingredient_unit == "tbsp":
            cost = price_per_ml * 14.7868 if price_per_ml else None
        elif ingredient_unit == "pc":
            cost = price_per_pc
        else:
            return None

        return cost

    def get_product_data(self, product_name):
        products_df = pd.read_csv(f"{self.path}/{self.products_file}")

        product_row = None
        for i, row in products_df.iterrows():
            if row["Product"] == product_name:
                pieces_made = products_df.at[i, "Pieces Made"]
                multiplier = products_df.at[i, "Multiplier"]
                product_row = row
                break

        if product_row is None:
            return None

        try:
            recipe_df = pd.read_csv(f"{self.path}/products/{product_name}.csv")
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Error loading product data: {e}.")
            return None

        return {
            "pieces_made": pieces_made,
            "multiplier": multiplier,
            "ingredients": recipe_df
        }

    def save_product_data(self, product_data):
        product_name = product_data["product_name"]
        pieces_made = product_data["pieces_made"]
        multiplier = product_data["multiplier"]
        recipe_list = product_data["ingredients"]
        try:
            products_df = pd.read_csv(f"{self.path}/{self.products_file}")
        except FileNotFoundError:
            products_df = pd.DataFrame(columns=["Product", "Pieces Made", "Multiplier"])
        products_df = products_df[products_df["Product"] != product_name]

        new_row = pd.DataFrame([{
            "Product": product_name,
            "Pieces Made": pieces_made,
            "Multiplier": multiplier
        }])
        products_df = pd.concat([products_df, new_row], ignore_index=True)
        products_df.to_csv(f"{self.path}/{self.products_file}", index=False)

        os.makedirs(f"{self.path}/products", exist_ok=True)

        recipe_df = pd.DataFrame.from_dict(recipe_list)
        recipe_df.to_csv(f"{self.path}/products/{product_name}.csv", index=False)

    def delete_product_data(self, product_name):
        try:
            products_df = pd.read_csv(f"{self.path}/{self.products_file}")
        except FileNotFoundError:
            raise FileNotFoundError("Products file not found.")

        if product_name not in products_df["Product"].values:
            raise ValueError(f"Product \"{product_name}\" not found.")

        products_df = products_df[products_df["Product"] != product_name]
        products_df.to_csv(f"{self.path}/{self.products_file}", index=False)

        recipe_file = f"{self.path}/products/{product_name}.csv"
        if os.path.exists(recipe_file):
            os.remove(recipe_file)

if __name__ == "__main__":
    main = AppMain()