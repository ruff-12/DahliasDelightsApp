import os
import pandas as pd

class AppMain:
    def __init__(self):
        self.path = os.getcwd()
        self.ingredients_file = "Ingredients.csv"
        self.products_file = "Products.csv"

    def get_ingredients_list(self):
        df = pd.read_csv(self.ingredients_file)
        data = df["Ingredient"].values.tolist()
        return data

    def get_products_list(self):
        df = pd.read_csv(self.products_file)
        data = df["Product"].values.tolist()
        return data

    def edit_ingredient_info(self, ingredient="", density="", brand="", cost="", amount="", unit=""):
        message = ""
        status = True

        if ingredient == "":
            message = "Invalid \"Ingredient\" - Please check."
            status = False
        elif density == "" or not density.replace(".", "", 1).isdigit():
            message = "Invalid \"Density (g/ml)\" - Please check."
            status = False
        elif brand == "":
            message = "Invalid \"Store Brand\" - Please check."
            status = False
        elif cost == "" or not cost.replace(".", "", 1).isdigit():
            message = "Invalid \"Store Cost (€)\" - Please check."
            status = False
        elif amount == "" or not amount.replace(".", "", 1).isdigit():
            message = "Invalid \"Store Amount\" - Please check."
            status = False
        elif unit == "":
            message = "Invalid \"Store Unit\" - Please check."
            status = False

        if status:
            df = pd.read_csv(self.ingredients_file)
            for i, row in df.iterrows():
                if row["Ingredient"] == ingredient:
                    try:
                        df.at[i, "Density (g/ml)"] = round(float(density), 2)
                        df.at[i, "Store Brand"] = brand
                        df.at[i, "Store Cost (€)"] = round(float(cost), 2)
                        df.at[i, "Store Amount"] = round(float(amount), 2)
                        df.at[i, "Store Unit"] = unit
                        df = df.sort_values(by="Ingredient")
                        df.to_csv(self.ingredients_file, mode="w", index=False)

                        message = f"{ingredient} information updated."
                    except Exception as e:
                        message = f"ERROR - {e}"
                        status = False
                    break
            else:
                df.loc[len(df)] = [
                    ingredient, round(float(density), 2), brand, round(float(cost), 2),
                    round(float(amount), 2), unit
                ]
                message = f"{ingredient} information added."

        return message, status

    def view_ingredient_info(self, ingredient=""):
        df = pd.read_csv(self.ingredients_file)
        density = 0.00
        brand = ""
        cost = 0.00
        amount = 0.00
        unit = ""
        for i, row in df.iterrows():
            if row["Ingredient"] == ingredient:
                density = df.at[i, "Density (g/ml)"]
                brand = df.at[i, "Store Brand"]
                cost = df.at[i, "Store Cost (€)"]
                amount = df.at[i, "Store Amount"]
                unit = df.at[i, "Store Unit"]
                break

        return density, brand, cost, amount, unit

    def view_costing_info(self, product):
        df = pd.read_csv(self.products_file)
        cost = 0.0
        pieces = 0.0
        multiplier = 0.0
        price = 0.0
        for i, row in df.iterrows():
            if row["Product"] == product:
                cost = df.at[i, "Production Cost (€)"]
                pieces = df.at[i, "Pieces Made"]
                multiplier = df.at[i, "Multiplier"]
                price = df.at[i, "Selling Price (€/pc)"]
                break

        return cost, pieces, multiplier, price

    def del_ingredient_info(self, ingredient):
        df = pd.read_csv(self.ingredients_file)
        for i, row in df.iterrows():
            if row["Ingredient"] == ingredient:
                try:
                    df.drop(index=i, inplace=True)
                    df = df.sort_values(by="Ingredient")
                    df.to_csv(self.ingredients_file, mode="w", index=False)

                    message = f"\"{ingredient}\" removed in database."
                    status = True
                except Exception as e:
                    message = f"ERROR - {e}"
                    status = False
                break
        else:
            message = f"\"{ingredient}\" not found in database."
            status = False

        return message, status

    def calculate_cost_table_row(self, ingredient, amount, unit):
        cost = 0.0
        message = ""
        status = True
        if ingredient == "":
            message = "Invalid \"Ingredient\" - Please check."
            status = False
        elif amount == "" or not amount.replace(".", "", 1).isdigit():
            message = "Invalid \"Amount Used\" - Please check."
            status = False
        elif unit == "":
            message = "Invalid \"Unit\" - Please check."
            status = False
        else:
            df = pd.read_csv(self.ingredients_file)
            for i, row in df.iterrows():
                if row["Ingredient"] == ingredient:
                    if pd.isnull(df.at[i, "Store Cost (€)"]):
                        message = f"No \"Store Cost (€)\" information for {ingredient} - Please add first."
                        status = False
                        break
                    if pd.isnull(df.at[i, "Store Amount"]):
                        message = f"No \"Store Amount\" information for {ingredient} - Please add first."
                        status = False
                        break
                    if pd.isnull(df.at[i, "Store Unit"]):
                        message = f"No \"Store Unit\" information for {ingredient} - Please add first."
                        status = False
                        break

                    cost_per_gram = 0.0
                    cost_per_piece = 0.0
                    if row["Store Unit"] == "grams":
                        cost_per_gram = float(df.at[i, "Store Cost (€)"]) / float(df.at[i, "Store Amount"])
                    elif row["Store Unit"] == "kilograms":
                        cost_per_gram = float(df.at[i, "Store Cost (€)"]) / (float(df.at[i, "Store Amount"]) * 1E3)
                    elif row["Store Unit"] == "pounds":
                        cost_per_gram = float(df.at[i, "Store Cost (€)"]) / (float(df.at[i, "Store Amount"]) * 453.6)
                    elif row["Store Unit"] == "milliliters":
                        cost_per_gram = float(df.at[i, "Store Cost (€)"]) / (float(df.at[i, "Store Amount"]) * float(df.at[i, "Average Density (g/ml)"]))
                    elif row["Store Unit"] == "liters":
                        cost_per_gram = float(df.at[i, "Store Cost (€)"]) / (float(df.at[i, "Store Amount"]) * 1E3 * float(df.at[i, "Average Density (g/ml)"]))
                    else:
                        cost_per_piece = float(df.at[i, "Store Cost (€)"]) / float(df.at[i, "Store Amount"])

                    if unit == "grams":
                        cost = cost_per_gram * float(amount)
                    elif unit == "kilograms":
                        cost = cost_per_gram * float(amount) * 1E3
                    elif unit == "pounds":
                        cost = cost_per_gram * float(amount) * 453.6
                    elif unit == "milliliters":
                        cost = cost_per_gram * float(amount) * float(row["Average Density (g/ml)"])
                    elif unit == "liters":
                        cost = cost_per_gram * float(amount) * 1E3 * float(row["Average Density (g/ml)"])
                    elif unit == "cups":
                        cost = cost_per_gram * float(amount) * 236.6 * float(row["Average Density (g/ml)"])
                    elif unit == "teaspoons":
                        cost = cost_per_gram * float(amount) * 4.929 * float(row["Average Density (g/ml)"])
                    elif unit == "tablespoons":
                        cost = cost_per_gram * float(amount) * 14.787 * float(row["Average Density (g/ml)"])
                    else:
                        cost = cost_per_piece * float(amount)

                    break
            else:
                message = f"\"{ingredient}\" not in list of Ingredients - Please add first."
                status = False

        return cost, message, status

    def calculate_selling_price(self, cost, pieces, multiplier):
        price = 0.0
        message = ""
        status = True
        if pieces == "0.0" or not pieces.replace(".", "", 1).isdigit():
            message = "Invalid \"Pieces Made\" - Please check."
            status = False
        else:
            price = cost * multiplier / pieces

        return price, message, status

    def save_product_costing(self, product, pieces, multiplier, total_cost, price, product_list):
        if product == "":
            message = "Invalid \"Product Name\" - Please check."
            status = False
        else:
            df = pd.read_csv(self.products_file)

            for i, row in df.iterrows():
                if row["Product"] == product:
                    df.at[i, "Production Cost (€)"] = round(float(total_cost), 2)
                    df.at[i, "Pieces Made"] = round(float(pieces), 1)
                    df.at[i, "Multiplier"] = round(float(multiplier), 1)
                    df.at[i, "Selling Price (€/pc)"] = round(float(price), 2)
                    break
            else:
                df.loc[len(df)] = [
                    product, round(float(total_cost), 2), round(float(pieces), 1),
                    round(float(multiplier), 1), round(float(price), 2)
                ]
            df.to_csv(self.products_file, index=False)

            df_new = pd.DataFrame(product_list, columns=["Ingredient", "Amount Used", "Unit", "Cost"])
            df_new.to_csv(f"{self.path}/products/{product}.csv", index=False)

            message = f"{product} saved."
            status = True

        return message, status

if __name__ == "__main__":
    main = AppMain()