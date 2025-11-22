import sys
import pandas as pd
from PySide6.QtCore import Qt
from AppMain import AppMain
from PySide6.QtWidgets import (QTabWidget, QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget,
                               QHBoxLayout, QPushButton, QTableWidgetItem, QComboBox, QMessageBox, QGridLayout,
                               QCompleter, QLineEdit)

class AppGUI(QMainWindow):
    """Main app window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dahlia's Delights")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)

        self.first_page = IngredientsPage()
        self.second_page = ProductsPage()

        self.tabs.addTab(self.first_page, "Ingredients")
        self.tabs.addTab(self.second_page, "Products/Costing")

        self.setCentralWidget(self.tabs)

class IngredientsPage(QWidget):
    """App page for Ingredients Management"""
    def __init__(self):
        super().__init__()
        self.app_main = AppMain()

        self.table = QTableWidget()

        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Ingredients Management")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        description = QLabel("This is where you edit your ingredients database")
        layout.addWidget(description)

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Ingredient", "Density (g/ml)", "Store Brand", "Store Price (€)", "Store Amount", "Store Unit"
        ])

        self.table.setColumnWidth(0, 180)  # Ingredient - wider for names
        self.table.setColumnWidth(1, 110)  # Density
        self.table.setColumnWidth(2, 150)  # Store Brand
        self.table.setColumnWidth(3, 110)  # Store Price
        self.table.setColumnWidth(4, 110)  # Store Amount
        self.table.setColumnWidth(5, 80)  # Store Unit

        self.table.setRowCount(1)

        layout.addWidget(self.table, stretch=1)

        button_layout = QHBoxLayout()

        add_row_btn = QPushButton("Add Row")
        add_row_btn.setStyleSheet("background-color: lightskyblue;")
        add_row_btn.clicked.connect(self.add_row)

        remove_row_btn = QPushButton("Remove Selected Row")
        remove_row_btn.setStyleSheet("background-color: lightpink;")
        remove_row_btn.clicked.connect(self.remove_row)

        save_btn = QPushButton("Save Ingredients Page")
        save_btn.setStyleSheet("background-color: lightgreen;")
        save_btn.clicked.connect(self.save_page)

        button_layout.addWidget(add_row_btn)
        button_layout.addWidget(remove_row_btn)
        button_layout.addWidget(save_btn)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_data(self):
        df = self.app_main.get_ingredients_df()

        if df is None or df.empty:
            return

        self.table.setRowCount(len(df))

        for row_idx, row in df.iterrows():
            for col_idx, column_name in enumerate(df.columns):
                if col_idx == 5:
                    self.add_unit_dropdown(row_idx, str(row[column_name])) if pd.notna(row[column_name]) else ""
                else:
                    value = str(row[column_name]) if pd.notna(row[column_name]) else ""
                    item = QTableWidgetItem(value)
                    self.table.setItem(row_idx, col_idx, item)

    def add_unit_dropdown(self, row, current_value=""):
        combo = QComboBox()
        units = ["g", "kg", "ml", "l", "oz", "lb", "pc"]
        combo.addItems(units)

        if current_value in units:
            combo.setCurrentText(current_value)
        elif current_value:
            combo.addItem(current_value)
            combo.setCurrentText(current_value)

        self.table.setCellWidget(row, 5, combo)

    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.add_unit_dropdown(row_position)

    def remove_row(self):
        current_row = self.table.currentRow()

        reply = QMessageBox.question(
            self, "Confirm Row Removal",
            f"Are you sure you want to remove row {current_row + 1}?",
            QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel
        )

        if reply == QMessageBox.Yes and current_row >= 0:
            self.table.removeRow(current_row)

    def save_page(self):
        validation_errors = self.validate_numeric_fields()

        if validation_errors:
            error_message = "Please fix the following errors:\n\n" + "\n".join(validation_errors)
            QMessageBox.warning(self, "Validation Error", error_message)
            return

        data = {}
        headers = []

        for col in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(col).text()
            headers.append(header)
            data[header] = []

        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                if col == 5:
                    widget = self.table.cellWidget(row, col)
                    value = widget.currentText() if widget else ""
                else:
                    item = self.table.item(row, col)
                    value = item.text() if item else ""
                data[headers[col]].append(value)

        self.app_main.update_ingredients_file(data)

        QMessageBox.information(self, "Success", "Ingredients saved successfully!")

    def validate_numeric_fields(self):
        errors = []

        for row in range(self.table.rowCount()):
            row_num = row + 1

            density_item = self.table.item(row, 1)
            if density_item and density_item.text().strip():
                try:
                    float(density_item.text().strip())
                except ValueError:
                    errors.append(f"Row {row_num}: Density must be a valid number.")

            price_item = self.table.item(row, 3)
            if price_item and price_item.text().strip():
                try:
                    float(price_item.text().strip())
                except ValueError:
                    errors.append(f"Row {row_num}: Store Price must be a valid number.")

            amount_item = self.table.item(row, 4)
            if amount_item and amount_item.text().strip():
                try:
                    float(amount_item.text().strip())
                except ValueError:
                    errors.append(f"Row {row_num}: Store Amount must be a valid number.")

        return errors

class ProductsPage(QWidget):
    """App page for Products Management"""
    def __init__(self):
        super().__init__()
        self.app_main = AppMain()

        self.product_name_dropdown = QComboBox()
        self.pieces_made_input = QLineEdit()
        self.multiplier_dropdown = QComboBox()
        self.product_cost_output = QLabel("0.00")
        self.product_price_output = QLabel("0.00")
        self.table = QTableWidget()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Products/Costing Management")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        description = QLabel("This is where you edit your products and costing")
        layout.addWidget(description)

        parameters_layout = QGridLayout()

        product_name_label = QLabel("Product Name:")
        self.product_name_dropdown.addItems(self.app_main.get_products_list())
        self.product_name_dropdown.setEditable(True)
        self.product_name_dropdown.completer().setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.product_name_dropdown.setMinimumWidth(200)
        self.product_name_dropdown.setMaximumWidth(300)
        parameters_layout.addWidget(product_name_label, 0, 0)
        parameters_layout.addWidget(self.product_name_dropdown, 1, 0)

        pieces_made_label = QLabel("Pieces Made:")
        self.pieces_made_input.setPlaceholderText("1.0")
        self.pieces_made_input.setFixedWidth(100)
        self.pieces_made_input.textChanged.connect(self.calculate_totals)
        parameters_layout.addWidget(pieces_made_label, 0, 1)
        parameters_layout.addWidget(self.pieces_made_input, 1, 1)

        multiplier_label = QLabel("Multiplier:")
        self.multiplier_dropdown.addItems(["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"])
        self.multiplier_dropdown.setCurrentIndex(5)
        self.multiplier_dropdown.setFixedWidth(80)
        self.multiplier_dropdown.currentTextChanged.connect(self.calculate_totals)
        parameters_layout.addWidget(multiplier_label, 0, 2)
        parameters_layout.addWidget(self.multiplier_dropdown, 1, 2)

        product_cost_label = QLabel("Production Cost (€):")
        self.product_cost_output.setStyleSheet("font-size: 18px;")
        self.product_cost_output.setMinimumWidth(100)
        parameters_layout.addWidget(product_cost_label, 0, 3)
        parameters_layout.addWidget(self.product_cost_output, 1, 3)

        product_price_label = QLabel("Product Price (€):")
        self.product_price_output.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.product_price_output.setMinimumWidth(100)
        parameters_layout.addWidget(product_price_label, 0, 4)
        parameters_layout.addWidget(self.product_price_output, 1, 4)

        parameters_layout.setColumnMinimumWidth(0, 220)  # Product Name
        parameters_layout.setColumnMinimumWidth(1, 120)  # Pieces Made
        parameters_layout.setColumnMinimumWidth(2, 100)  # Multiplier
        parameters_layout.setColumnMinimumWidth(3, 150)  # Production Cost
        parameters_layout.setColumnMinimumWidth(4, 150)  # Product Price

        parameters_layout.setColumnStretch(5, 1)

        layout.addLayout(parameters_layout)

        button_layout = QHBoxLayout()

        load_product_btn = QPushButton("Load Product Info")
        load_product_btn.setStyleSheet("background-color: lightcyan;")
        load_product_btn.clicked.connect(self.load_product_info)

        save_product_btn = QPushButton("Save Product Info")
        save_product_btn.setStyleSheet("background-color: lemonchiffon;")
        save_product_btn.clicked.connect(self.save_product_info)

        delete_product_btn = QPushButton("Delete Product Info")
        delete_product_btn.setStyleSheet("background-color: lavenderblush;")
        delete_product_btn.clicked.connect(self.delete_product_info)

        button_layout.addWidget(load_product_btn)
        button_layout.addWidget(save_product_btn)
        button_layout.addWidget(delete_product_btn)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Ingredient", "Amount Used", "Amount Unit", "Ingredient Cost (€)"
        ])

        self.table.setColumnWidth(0, 300)  # Ingredient - wider for names
        self.table.setColumnWidth(1, 160)  # Amount Used
        self.table.setColumnWidth(2, 100)  # Amount Unit
        self.table.setColumnWidth(3, 180)  # Ingredient Cost

        self.table.itemChanged.connect(self.calculate_row_cost)

        self.add_row()

        layout.addWidget(self.table, stretch=1)

        table_button_layout = QHBoxLayout()

        add_row_btn = QPushButton("Add Row")
        add_row_btn.setStyleSheet("background-color: lightskyblue;")
        add_row_btn.clicked.connect(self.add_row)

        remove_row_btn = QPushButton("Remove Selected Row")
        remove_row_btn.setStyleSheet("background-color: lightpink;")
        remove_row_btn.clicked.connect(self.remove_row)

        table_button_layout.addWidget(add_row_btn)
        table_button_layout.addWidget(remove_row_btn)
        table_button_layout.addStretch()

        layout.addLayout(table_button_layout)

        layout.addStretch()

        self.setLayout(layout)

    def load_product_info(self):
        product_name = self.product_name_dropdown.currentText()

        if not product_name:
            QMessageBox.warning(self, "No Product Selected", "Please select a \"Product Name\" first")
            return

        product_data_dict = self.app_main.get_product_data(product_name)

        if product_data_dict is None:
            QMessageBox.warning(self, "Product Not Found", f"No data found for product: {product_name}.")
            return

        self.table.setRowCount(0)

        self.pieces_made_input.setText(str(product_data_dict["pieces_made"]))

        multiplier_text = str(product_data_dict["multiplier"])
        index = self.multiplier_dropdown.findText(multiplier_text)
        if index >= 0:
            self.multiplier_dropdown.setCurrentIndex(index)
        else:
            self.multiplier_dropdown.addItem(multiplier_text)
            self.multiplier_dropdown.setCurrentText(multiplier_text)

        ingredients_df = product_data_dict["ingredients"]

        for i, row in ingredients_df.iterrows():
            self.add_row()

            current_row = self.table.rowCount() - 1

            ingredient_widget = self.table.cellWidget(current_row, 0)
            if ingredient_widget:
                ingredient_widget.setCurrentText(row["Ingredient"])

            amount_item = self.table.item(current_row, 1)
            if amount_item:
                amount_item.setText(str(row["Amount Used"]))

            unit_widget = self.table.cellWidget(current_row, 2)
            if unit_widget:
                unit_widget.setCurrentText(row["Amount Unit"])

        self.calculate_row_cost()

        QMessageBox.information(self, "Success", f"Loaded product: {product_name}.")

    def save_product_info(self):
        product_name = self.product_name_dropdown.currentText().strip()
        if not product_name:
            QMessageBox.warning(self, "No Product Name", "Please enter a \"Product Name\" first.")
            return

        pieces_text = self.pieces_made_input.text().strip()
        if not pieces_text:
            QMessageBox.warning(self, "Missing Pieces Made", "Please enter \"Pieces Made\" value.")
            return
        try:
            pieces_made = float(pieces_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Pieces Made", "\"Pieces Made\" must be a valid number.")
            return

        try:
            multiplier = float(self.multiplier_dropdown.currentText())
        except ValueError:
            QMessageBox.warning(self, "Invalid Multiplier", "\"Multiplier\" must be a valid number.")

        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "No Ingredients", "Please add at least one ingredient.")
            return

        ingredients_data = []
        for row in range(self.table.rowCount()):
            ingredient_widget = self.table.cellWidget(row, 0)
            amount_item = self.table.item(row, 1)
            unit_widget = self.table.cellWidget(row, 2)
            if not ingredient_widget or not amount_item or not unit_widget:
                continue

            ingredient_name = ingredient_widget.currentText().strip()
            amount_text = amount_item.text().strip()
            unit = unit_widget.currentText()
            if not ingredient_name or not amount_text:
                continue

            try:
                amount_used = float(amount_text)
            except ValueError:
                QMessageBox.warning(self, "Invalid Amount Used", f"Row: {row + 1}: \"Amount Used\" must be a valid number.")
                return

            ingredients_data.append({
                "Ingredient": ingredient_name,
                "Amount Used": amount_used,
                "Amount Unit": unit
            })
        if not ingredients_data:
            QMessageBox.warning(self, "No Valid Ingredients", "Please add at least one valid ingredient.")
            return

        product_data = {
            "product_name": product_name,
            "pieces_made": pieces_made,
            "multiplier": multiplier,
            "ingredients": ingredients_data
        }

        try:
            self.app_main.save_product_data(product_data)

            if self.product_name_dropdown.findText(product_name) == -1:
                self.product_name_dropdown.addItem(product_name)

            QMessageBox.information(self, "Success", f"Product \"{product_name}\" saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save product: {str(e)}.")

    def delete_product_info(self):
        product_name = self.product_name_dropdown.currentText().strip()
        if not product_name:
            QMessageBox.warning(self, "No Product Selected", "Please select a \"Product Name\" first.")
            return

        product_data = self.app_main.get_product_data(product_name)
        if product_data is None:
            QMessageBox.warning(self, "Product Not Found", f"Product: {product_name} does not exist.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete product \"{product_name}\"?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.app_main.delete_product_data(product_name)

                self.pieces_made_input.clear()
                self.multiplier_dropdown.setCurrentIndex(5)
                self.table.setRowCount(0)
                self.add_row()
                self.product_cost_output.setText("0.00")
                self.product_price_output.setText("0.00")

                index = self.product_name_dropdown.findText(product_name)
                if index >= 0:
                    self.product_name_dropdown.removeItem(index)

                QMessageBox.information(self, "Success", f"Product \"{product_name}\" deleted successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Delete Error", f"Failed to delete product: {str(e)}.")

    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        ingredient_dropdown = QComboBox()
        ingredient_dropdown.addItems(self.app_main.get_ingredient_list())
        ingredient_dropdown.setEditable(True)
        ingredient_dropdown.completer().setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        ingredient_dropdown.currentTextChanged.connect(self.calculate_row_cost)
        self.table.setCellWidget(row_position, 0, ingredient_dropdown)

        amount_item = QTableWidgetItem("0.00")
        self.table.setItem(row_position, 1, amount_item)

        unit_dropdown = QComboBox()
        unit_dropdown.addItems(["g", "kg", "oz", "lb", "ml", "l", "cup", "tsp", "tbsp", "pc"])
        unit_dropdown.currentTextChanged.connect(self.calculate_row_cost)
        self.table.setCellWidget(row_position, 2, unit_dropdown)

        cost_item = QTableWidgetItem("0.00")
        cost_item.setFlags(cost_item.flags() & ~Qt.ItemIsEditable)
        cost_item.setBackground(Qt.lightGray)
        self.table.setItem(row_position, 3, cost_item)

    def calculate_row_cost(self):
        for row in range(self.table.rowCount()):
            ingredient_widget = self.table.cellWidget(row, 0)
            if not ingredient_widget:
                continue
            ingredient_name = ingredient_widget.currentText()

            amount_item = self.table.item(row, 1)
            if not amount_item or not amount_item.text().strip():
                continue
            try:
                amount_used = float(amount_item.text().strip())
            except ValueError:
                continue

            unit_widget = self.table.cellWidget(row, 2)
            if not unit_widget:
                continue
            unit = unit_widget.currentText()

            cost_per_unit = self.app_main.get_ingredient_cost(ingredient_name, unit)

            if cost_per_unit is not None:
                ingredient_cost = amount_used * cost_per_unit

                cost_item = self.table.item(row, 3)
                if cost_item:
                    cost_item.setText(f"{ingredient_cost:.4f}")

        self.calculate_totals()

    def calculate_totals(self):
        total_cost = 0.0

        for row in range(self.table.rowCount()):
            cost_item = self.table.item(row, 3)
            if cost_item and cost_item.text():
                try:
                    total_cost += float(cost_item.text())
                except ValueError:
                    continue

        pieces_text = self.pieces_made_input.text().strip()
        pieces_made = 1.0
        if pieces_text:
            try:
                pieces_made = float(pieces_text)
            except ValueError:
                pieces_made = 1.0

        if pieces_made > 0:
            production_cost = total_cost / pieces_made
        else:
            production_cost = 0.0

        try:
            multiplier = float(self.multiplier_dropdown.currentText())
        except ValueError:
            multiplier = 1.0

        product_price = production_cost * multiplier

        self.product_cost_output.setText(f"{production_cost:.2f}")
        self.product_price_output.setText(f"{product_price:.2f}")

    def remove_row(self):
        current_row = self.table.currentRow()

        reply = QMessageBox.question(
            self, "Confirm Row Removal",
            f"Are you sure you want to remove row {current_row + 1}?",
            QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel
        )

        if reply == QMessageBox.Yes and current_row >= 0:
            self.table.removeRow(current_row)
            self.calculate_totals()

def main():
    app = QApplication(sys.argv)
    window = AppGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()