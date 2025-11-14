import sys
import pandas as pd
from AppMain import AppMain
from PySide6.QtWidgets import (QTabWidget, QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget,
                               QHBoxLayout, QPushButton, QTableWidgetItem, QComboBox, QMessageBox)

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
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Ingredients Management")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        description = QLabel("This is where you edit your ingredients database")
        layout.addWidget(description)

        self.table = QTableWidget()
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
        add_row_btn.clicked.connect(self.add_row)

        remove_row_btn = QPushButton("Remove Selected Row")
        remove_row_btn.clicked.connect(self.remove_row)

        save_btn = QPushButton("Save Ingredients Page")
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
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Products/Costing Management")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        description = QLabel("This is where you edit your products and costing")

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()

        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = AppGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()