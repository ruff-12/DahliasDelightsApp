import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QLabel,
                               QFrame, QComboBox, QCompleter, QLineEdit, QGridLayout, QMessageBox, QTableWidget,
                               QHeaderView, QDialog, QTableWidgetItem)
from AppMain import AppMain


class AppGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # import external scripts
        self.main = AppMain()
        # window title and size
        self.setWindowTitle("Dahlia's Delights")
        self.setGeometry(100, 100, 1000, 700)  # x, y, width, height
        # set main widget and layout
        main_layout = QHBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        # create the left and right sections
        self.create_main_menu(main_layout)
        self.create_content_area(main_layout)
        # create message box
        self.message_box = QLabel("")
        self.message_box.setWordWrap(True)

    def create_main_menu(self, main_layout):
        menu_widget = QWidget()
        menu_widget.setFixedWidth(150)
        menu_widget.setStyleSheet("QWidget {border-right: 2px solid black;}")
        menu_layout = QVBoxLayout()
        menu_widget.setLayout(menu_layout)
        # create menu buttons
        menu_btn1 = QPushButton("Ingredients")
        menu_btn2 = QPushButton("Costing")
        # connect buttons to functions
        menu_btn1.clicked.connect(self.show_ingredients_page)
        menu_btn2.clicked.connect(self.show_costing_page)
        # add widgets to layout
        menu_layout.addWidget(menu_btn1)
        menu_layout.addWidget(menu_btn2)
        menu_layout.addStretch()
        # add main widget to main layout
        main_layout.addWidget(menu_widget)

    def create_content_area(self, main_layout):
        self.content_widget = QWidget()
        content_layout = QVBoxLayout()
        self.content_widget.setLayout(content_layout)
        # create widgets
        welcome_title = QLabel("Welcome to Dahlia's Delights!")
        welcome_title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 5px;")
        welcome_note = QLabel("Please click a button on the left menu to start.")
        welcome_note.setStyleSheet("padding: 5px;")
        # add widgets to layout
        content_layout.addWidget(welcome_title)
        content_layout.addWidget(welcome_note)
        content_layout.addStretch()
        # add content widget to main layout
        main_layout.addWidget(self.content_widget)

    def set_message_box(self, message="", status=True):
        if status:
            self.message_box.setText(f"✓ {message}")
            self.message_box.setStyleSheet("background-color: lightgreen; color: darkgreen; padding: 5px;")
        else:
            self.message_box.setText(f"✗ {message}")
            self.message_box.setStyleSheet("background-color: pink; color: darkred; padding: 5px;")

    def show_ingredients_page(self):
        ingredients_widget = QWidget()
        ingredients_layout = QVBoxLayout()
        ingredients_widget.setLayout(ingredients_layout)

        # title
        title = QLabel("Manage Ingredients")
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 5px;")
        ingredients_layout.addWidget(title)

        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        ingredients_layout.addWidget(sep1)

        # edit ingredients
        edit_ingredients_title = QLabel("Use the form below to add/change ingredient values.")
        ingredients_layout.addWidget(edit_ingredients_title)

        edit_ingredients_widget = QWidget()
        edit_ingredients_layout = QGridLayout()
        edit_ingredients_widget.setLayout(edit_ingredients_layout)

        edit_ingredient_label = QLabel("Ingredient:")
        edit_ingredient_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_ingredient_dropdown = QComboBox()
        self.edit_ingredient_dropdown.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_ingredient_dropdown.addItems(self.main.get_ingredients_list())
        self.edit_ingredient_dropdown.setEditable(True)
        self.edit_ingredient_dropdown.completer().setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        edit_ingredients_layout.addWidget(edit_ingredient_label, 0, 0)
        edit_ingredients_layout.addWidget(self.edit_ingredient_dropdown, 1, 0)

        edit_density_label = QLabel("Density (g/ml):")
        edit_density_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_density_input = QLineEdit()
        self.edit_density_input.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_density_input.setPlaceholderText("0.0")
        edit_ingredients_layout.addWidget(edit_density_label, 0, 1)
        edit_ingredients_layout.addWidget(self.edit_density_input, 1, 1)

        edit_store_brand_label = QLabel("Store Brand:")
        edit_store_brand_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_store_brand_input = QLineEdit()
        self.edit_store_brand_input.setStyleSheet("max-width: 120px; padding: 5px;")
        edit_ingredients_layout.addWidget(edit_store_brand_label, 0, 2)
        edit_ingredients_layout.addWidget(self.edit_store_brand_input, 1, 2)

        edit_store_cost_label = QLabel("Store Cost (€):")
        edit_store_cost_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_store_cost_input = QLineEdit()
        self.edit_store_cost_input.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_store_cost_input.setPlaceholderText("0.00")
        edit_ingredients_layout.addWidget(edit_store_cost_label, 0, 3)
        edit_ingredients_layout.addWidget(self.edit_store_cost_input, 1, 3)

        edit_store_amount_label = QLabel("Store Amount:")
        edit_store_amount_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_store_amount_input = QLineEdit()
        self.edit_store_amount_input.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_store_amount_input.setPlaceholderText("0.0")
        edit_ingredients_layout.addWidget(edit_store_amount_label, 0, 4)
        edit_ingredients_layout.addWidget(self.edit_store_amount_input, 1, 4)

        edit_store_unit_label = QLabel("Store Unit:")
        edit_store_unit_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_store_unit_dropdown = QComboBox()
        self.edit_store_unit_dropdown.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_store_unit_dropdown.addItems(["grams", "kilograms", "pounds", "milliliters", "liters", "pieces"])
        edit_ingredients_layout.addWidget(edit_store_unit_label, 0, 5)
        edit_ingredients_layout.addWidget(self.edit_store_unit_dropdown, 1, 5)

        edit_ingredients_layout.setColumnStretch(6, 1)

        ingredients_layout.addWidget(edit_ingredients_widget)

        edit_ingredients_btn = QPushButton("Add/Edit Ingredient Info")
        edit_ingredients_btn.setStyleSheet("max-width: 200px; padding: 5px;")
        edit_ingredients_btn.clicked.connect(self.edit_ingredient_info)
        ingredients_layout.addWidget(edit_ingredients_btn)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        ingredients_layout.addWidget(sep2)

        # view ingredients
        view_ingredients_title = QLabel("Use the form below to view ingredient values.")
        ingredients_layout.addWidget(view_ingredients_title)

        view_ingredients_widget = QWidget()
        view_ingredients_layout = QGridLayout()
        view_ingredients_widget.setLayout(view_ingredients_layout)

        view_ingredient_label = QLabel("Ingredient:")
        view_ingredient_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.view_ingredient_dropdown = QComboBox()
        self.view_ingredient_dropdown.setStyleSheet("max-width: 120px; padding: 5px;")
        self.view_ingredient_dropdown.addItems(self.main.get_ingredients_list())
        view_ingredients_layout.addWidget(view_ingredient_label, 0, 0)
        view_ingredients_layout.addWidget(self.view_ingredient_dropdown, 1, 0)

        view_density_label = QLabel("Density (g/ml):")
        view_density_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.view_density_output = QLabel("0.00 g/ml")
        self.view_density_output.setStyleSheet("font-size: 18px; max-width: 120px; padding: 5px;")
        view_ingredients_layout.addWidget(view_density_label, 0, 1)
        view_ingredients_layout.addWidget(self.view_density_output, 1, 1)

        view_store_brand_label = QLabel("Store Brand:")
        view_store_brand_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.view_store_brand_output = QLabel("")
        self.view_store_brand_output.setStyleSheet("font-size: 18px; max-width: 120px; padding: 5px;")
        view_ingredients_layout.addWidget(view_store_brand_label, 0, 2)
        view_ingredients_layout.addWidget(self.view_store_brand_output, 1, 2)

        view_store_cost_label = QLabel("Store Cost (€):")
        view_store_cost_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.view_store_cost_output = QLabel("€ 0.00")
        self.view_store_cost_output.setStyleSheet("font-size: 18px; max-width: 120px; padding: 5px;")
        view_ingredients_layout.addWidget(view_store_cost_label, 0, 3)
        view_ingredients_layout.addWidget(self.view_store_cost_output, 1, 3)

        view_store_amount_label = QLabel("Store Amount:")
        view_store_amount_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.view_store_amount_output = QLabel("0.00")
        self.view_store_amount_output.setStyleSheet("font-size: 18px; max-width: 120px; padding: 5px;")
        view_ingredients_layout.addWidget(view_store_amount_label, 0, 4)
        view_ingredients_layout.addWidget(self.view_store_amount_output, 1, 4)

        view_store_unit_label = QLabel("Store Unit:")
        view_store_unit_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.view_store_unit_output = QLabel("")
        self.view_store_unit_output.setStyleSheet("font-size: 18px; max-width: 120px; padding: 5px;")
        view_ingredients_layout.addWidget(view_store_unit_label, 0, 5)
        view_ingredients_layout.addWidget(self.view_store_unit_output, 1, 5)

        view_ingredients_layout.setColumnStretch(6, 1)

        ingredients_layout.addWidget(view_ingredients_widget)

        view_ingredients_btn = QPushButton("View Ingredient Info")
        view_ingredients_btn.setStyleSheet("max-width: 200px; padding: 5px;")
        view_ingredients_btn.clicked.connect(self.view_ingredient_info)
        ingredients_layout.addWidget(view_ingredients_btn)

        sep3 = QFrame()
        sep3.setFrameShape(QFrame.HLine)
        ingredients_layout.addWidget(sep3)

        # delete ingredient
        del_ingredients_title = QLabel("Use the form below to delete ingredient values.")
        ingredients_layout.addWidget(del_ingredients_title)

        del_ingredients_widget = QWidget()
        del_ingredients_layout = QHBoxLayout()
        del_ingredients_widget.setLayout(del_ingredients_layout)

        del_ingredient_label = QLabel("Ingredient:")
        del_ingredient_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.del_ingredient_dropdown = QComboBox()
        self.del_ingredient_dropdown.setStyleSheet("max-width: 120px; padding: 5px;")
        self.del_ingredient_dropdown.addItems(self.main.get_ingredients_list())
        self.del_ingredient_dropdown.setEditable(True)
        self.del_ingredient_dropdown.completer().setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        del_ingredients_layout.addWidget(del_ingredient_label)
        del_ingredients_layout.addWidget(self.del_ingredient_dropdown)

        del_ingredients_btn = QPushButton("Delete Ingredient Info")
        del_ingredients_btn.setStyleSheet("max-width: 200px; padding: 5px;")
        del_ingredients_btn.clicked.connect(self.del_ingredient_info)
        del_ingredients_layout.addWidget(del_ingredients_btn)

        del_ingredients_layout.addStretch()

        ingredients_layout.addWidget(del_ingredients_widget)

        sep4 = QFrame()
        sep4.setFrameShape(QFrame.HLine)
        ingredients_layout.addWidget(sep4)

        # add message box
        ingredients_layout.addWidget(self.message_box)
        ingredients_layout.addStretch()

        # replace content widget
        self.content_widget.hide()
        self.content_widget.deleteLater()
        self.content_widget = ingredients_widget
        self.centralWidget().layout().addWidget(self.content_widget)

    def edit_ingredient_info(self):
        ingredient = self.edit_ingredient_dropdown.currentText()

        reply = QMessageBox.question(
            self, "Confirm Edit",
            f"Are you sure you want to Add/Change \"{ingredient}\" values?",
            QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel
        )
        if reply == QMessageBox.Yes:
            density = self.edit_density_input.text()
            brand = self.edit_store_brand_input.text()
            cost = self.edit_store_cost_input.text()
            amount = self.edit_store_amount_input.text()
            unit = self.edit_store_unit_dropdown.currentText()

            message, status = self.main.edit_ingredient_info(ingredient, density, brand, cost, amount, unit)
            self.set_message_box(message, status)

            if status:
                self.update_ingredient_dropdowns()
        else:
            self.set_message_box("Add/Change Operation Cancelled", True)

    def view_ingredient_info(self):
        ingredient = self.view_ingredient_dropdown.currentText()
        density, brand, cost, amount, unit = self.main.view_ingredient_info(ingredient)

        self.view_density_output.setText(f"{density} g/ml")
        self.view_store_brand_output.setText(brand)
        self.view_store_cost_output.setText(f"€ {cost}")
        self.view_store_amount_output.setText(f"{amount}")
        self.view_store_unit_output.setText(unit)

        self.set_message_box(f"\"{ingredient}\" values successfully pulled", True)

    def del_ingredient_info(self):
        ingredient = self.del_ingredient_dropdown.currentText()

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to Delete \"{ingredient}\" values?\nThis cannot be undone.",
            QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel
        )
        if reply == QMessageBox.Yes:
            message, status = self.main.del_ingredient_info(ingredient)
            self.set_message_box(message, status)

            if status:
                self.update_ingredient_dropdowns()
        else:
            self.set_message_box("Delete Operation Cancelled", True)

    def update_ingredient_dropdowns(self):
        self.edit_ingredient_dropdown.addItems(self.main.get_ingredients_list())
        self.view_ingredient_dropdown.addItems(self.main.get_ingredients_list())
        self.del_ingredient_dropdown.addItems(self.main.get_ingredients_list())
        self.table_ingredient_dropdown.addItems(self.main.get_ingredients_list())

    def show_costing_page(self):
        costing_widget = QWidget()
        costing_layout = QVBoxLayout()
        costing_widget.setLayout(costing_layout)

        # title
        title = QLabel("Manage Product Costing")
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 5px;")
        costing_layout.addWidget(title)

        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        costing_layout.addWidget(sep1)

        # view product costing
        view_costing_title = QLabel("Use the form below to view product costing values.")
        costing_layout.addWidget(view_costing_title)

        view_costing_widget = QWidget()
        view_costing_layout = QGridLayout()
        view_costing_widget.setLayout(view_costing_layout)

        view_product_label = QLabel("Product Name:")
        view_product_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.view_product_dropdown = QComboBox()
        self.view_product_dropdown.setStyleSheet("max-width: 120px; padding: 5px;")
        self.view_product_dropdown.addItems(self.main.get_products_list())
        view_costing_layout.addWidget(view_product_label, 0, 0)
        view_costing_layout.addWidget(self.view_product_dropdown, 1, 0)

        view_pieces_label = QLabel("Pieces Made:")
        view_pieces_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.view_pieces_output = QLabel("0")
        self.view_pieces_output.setStyleSheet("font-size: 18px; max-width: 120px; padding: 5px;")
        view_costing_layout.addWidget(view_pieces_label, 0, 1)
        view_costing_layout.addWidget(self.view_pieces_output, 1, 1)

        view_multiplier_label = QLabel("Cost Multiplier:")
        view_multiplier_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.view_multiplier_output = QLabel("x 0.0")
        self.view_multiplier_output.setStyleSheet("font-size: 18px; max-width: 120px; padding: 5px;")
        view_costing_layout.addWidget(view_multiplier_label, 0, 2)
        view_costing_layout.addWidget(self.view_multiplier_output, 1, 2)

        view_cost_label = QLabel("Production Cost:")
        view_cost_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.view_cost_output = QLabel("€ 0.00")
        self.view_cost_output.setStyleSheet("font-size: 18px; max-width: 120px; padding: 5px;")
        view_costing_layout.addWidget(view_cost_label, 0, 3)
        view_costing_layout.addWidget(self.view_cost_output, 1, 3)

        view_price_label = QLabel("Selling Price:")
        view_price_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.view_price_output = QLabel("€ 0.00 / pc")
        self.view_price_output.setStyleSheet("font-size: 18px; max-width: 120px; padding: 5px;")
        view_costing_layout.addWidget(view_price_label, 0, 4)
        view_costing_layout.addWidget(self.view_price_output, 1, 4)

        view_costing_layout.setColumnStretch(5, 1)

        costing_layout.addWidget(view_costing_widget)

        view_costing_btn = QPushButton("View Costing Info")
        view_costing_btn.setStyleSheet("max-width: 200px; padding: 5px;")
        view_costing_btn.clicked.connect(self.view_costing_info)
        costing_layout.addWidget(view_costing_btn)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        costing_layout.addWidget(sep2)

        # edit product costing
        view_costing_title = QLabel("Use the form below to add/change product costing values.")
        costing_layout.addWidget(view_costing_title)

        edit_costing_widget = QWidget()
        edit_costing_layout = QGridLayout()
        edit_costing_widget.setLayout(edit_costing_layout)

        edit_product_label = QLabel("Product Name:")
        edit_product_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_product_dropdown = QComboBox()
        self.edit_product_dropdown.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_product_dropdown.addItems(self.main.get_products_list())
        self.edit_product_dropdown.setEditable(True)
        self.edit_product_dropdown.completer().setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        edit_costing_layout.addWidget(edit_product_label, 0, 0)
        edit_costing_layout.addWidget(self.edit_product_dropdown, 1, 0)

        edit_pieces_label = QLabel("Pieces Made:")
        edit_pieces_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_pieces_output = QLineEdit()
        self.edit_pieces_output.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_pieces_output.setPlaceholderText("0.0")
        edit_costing_layout.addWidget(edit_pieces_label, 0, 1)
        edit_costing_layout.addWidget(self.edit_pieces_output, 1, 1)

        edit_multiplier_label = QLabel("Cost Multiplier:")
        edit_multiplier_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_multiplier_dropdown = QComboBox()
        self.edit_multiplier_dropdown.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_multiplier_dropdown.addItems(["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"])
        self.edit_multiplier_dropdown.setCurrentIndex(5)
        edit_costing_layout.addWidget(edit_multiplier_label, 0, 2)
        edit_costing_layout.addWidget(self.edit_multiplier_dropdown, 1, 2)

        edit_cost_label = QLabel("Production Cost:")
        edit_cost_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_cost_output = QLabel("€ 0.00")
        self.edit_cost_output.setStyleSheet("font-size: 18px; max-width: 120px; padding: 5px;")
        edit_costing_layout.addWidget(edit_cost_label, 0, 3)
        edit_costing_layout.addWidget(self.edit_cost_output, 1, 3)

        edit_price_label = QLabel("Selling Price:")
        edit_price_label.setStyleSheet("max-width: 120px; padding: 5px;")
        self.edit_price_output = QLabel("€ 0.00 / pc")
        self.edit_price_output.setStyleSheet("font-size: 18px; max-width: 120px; padding: 5px;")
        edit_costing_layout.addWidget(edit_price_label, 0, 4)
        edit_costing_layout.addWidget(self.edit_price_output, 1, 4)

        edit_costing_layout.setColumnStretch(5, 1)

        costing_layout.addWidget(edit_costing_widget)

        edit_table_widget = QWidget()
        edit_table_layout = QHBoxLayout()
        edit_table_widget.setLayout(edit_table_layout)

        self.costing_table = QTableWidget()
        self.costing_table.setColumnCount(6)
        self.costing_table.setHorizontalHeaderLabels([
            "Ingredient", "Amount Used", "Unit", "Calc/Edit", "Cost (€)", "Delete Row"
        ])
        self.costing_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.costing_table.setMaximumHeight(300)
        self.costing_table.setStyleSheet("border: 1px solid black;")

        self.add_costing_table_row()

        edit_table_layout.addWidget(self.costing_table)

        add_table_row_btn = QPushButton("Add Row")
        add_table_row_btn.setStyleSheet("background-color: green; color: white; border-radius: 5px; padding: 5px;")
        add_table_row_btn.clicked.connect(self.add_costing_table_row)
        edit_table_layout.addWidget(add_table_row_btn)

        costing_layout.addWidget(edit_table_widget)

        calc_and_save_widget = QWidget()
        calc_and_save_layout = QHBoxLayout()
        calc_and_save_widget.setLayout(calc_and_save_layout)

        calc_total_cost_btn = QPushButton("Calculate Total Cost")
        calc_total_cost_btn.setStyleSheet("max-width: 200px; padding: 5px;")
        calc_total_cost_btn.clicked.connect(self.calculate_total_cost)
        calc_and_save_layout.addWidget(calc_total_cost_btn)

        save_product_cost_btn = QPushButton("Save Product Costing")
        save_product_cost_btn.setStyleSheet("max-width: 200px; padding: 5px;")
        save_product_cost_btn.clicked.connect(self.save_product_costing)
        calc_and_save_layout.addWidget(save_product_cost_btn)

        calc_and_save_layout.addStretch()

        costing_layout.addWidget(calc_and_save_widget)

        # add message box
        costing_layout.addWidget(self.message_box)
        costing_layout.addStretch()

        # replace content widget
        self.content_widget.hide()
        self.content_widget.deleteLater()
        self.content_widget = costing_widget
        self.centralWidget().layout().addWidget(self.content_widget)

    def view_costing_info(self):
        product = self.view_product_dropdown.currentText()
        cost, pieces, multiplier, price = self.main.view_costing_info(product)

        self.view_cost_output.setText(f"€ {cost}")
        self.view_pieces_output.setText(f"{pieces}")
        self.view_multiplier_output.setText(f"x {multiplier}")
        self.view_price_output.setText(f"€ {price} / pc")

        self.set_message_box(f"\"{product}\" values successfully pulled", True)

        popup = TablePopup(product, self)
        popup.exec()

    def add_costing_table_row(self):
        row_position = self.costing_table.rowCount()
        self.costing_table.insertRow(row_position)

        self.cost_table_ingredient_dropdown = QComboBox()
        self.cost_table_ingredient_dropdown.addItems(self.main.get_ingredients_list())
        self.costing_table.setCellWidget(row_position, 0, self.cost_table_ingredient_dropdown)

        self.cost_table_amount_input = QLineEdit()
        self.cost_table_amount_input.setPlaceholderText("0.00")
        self.costing_table.setCellWidget(row_position, 1, self.cost_table_amount_input)

        self.cost_table_unit_dropdown = QComboBox()
        self.cost_table_unit_dropdown.addItems([
            "grams", "kilograms", "pounds", "milliliters", "liters", "cups", "teaspoons", "tablespoons", "pieces"
        ])
        self.costing_table.setCellWidget(row_position, 2, self.cost_table_unit_dropdown)

        cost_calculate_btn = QPushButton("Calc/Edit")
        cost_calculate_btn.setStyleSheet("background-color: blue; color: white; border-radius: 5px; padding: 5px;")
        cost_calculate_btn.clicked.connect(self.calculate_cost_from_button)
        self.costing_table.setCellWidget(row_position, 3, cost_calculate_btn)

        self.cost_table_cost_output = QLabel("0.0000")
        self.cost_table_cost_output.setStyleSheet("padding: 5px;")
        self.costing_table.setCellWidget(row_position, 4, self.cost_table_cost_output)

        cost_del_row_btn = QPushButton("Delete Row")
        cost_del_row_btn.setStyleSheet("background-color: red; color: white; border-radius: 5px; padding: 5px;")
        cost_del_row_btn.clicked.connect(self.delete_cost_from_button)
        self.costing_table.setCellWidget(row_position, 5, cost_del_row_btn)

    def delete_cost_from_button(self):
        button = self.sender()
        for row in range(self.costing_table.rowCount()):
            if self.costing_table.cellWidget(row, 5) == button:
                self.delete_cost_table_row(row)
                break

    def delete_cost_table_row(self, row):
        self.costing_table.removeRow(row)

    def calculate_cost_from_button(self):
        button = self.sender()
        for row in range(self.costing_table.rowCount()):
            if self.costing_table.cellWidget(row, 3) == button:
                self.calculate_cost_table_row(row)
                break

    def calculate_cost_table_row(self, row):
        ingredient_dropdown = self.costing_table.cellWidget(row, 0)
        ingredient = ingredient_dropdown.currentText()
        amount_input = self.costing_table.cellWidget(row, 1)
        amount = amount_input.text()
        unit_dropdown = self.costing_table.cellWidget(row, 2)
        unit = unit_dropdown.currentText()

        line_cost, message, status = self.main.calculate_cost_table_row(ingredient, amount, unit)

        if status:
            cost_label = self.costing_table.cellWidget(row, 4)
            cost_label.setText(f"{line_cost:.4f}")

            #self.total_cost += line_cost
        else:
            self.set_message_box(message, status)

        return line_cost

    def calculate_total_cost(self):
        total_cost = 0.0
        for row in range(self.costing_table.rowCount()):
            line_cost = self.calculate_cost_table_row(row)
            total_cost = total_cost + line_cost

        self.edit_cost_output.setText(f"€ {total_cost:.2f}")

        pieces = self.edit_pieces_output.text()
        multiplier = self.edit_multiplier_dropdown.currentText()

        price, message, status = self.main.calculate_selling_price(total_cost, pieces, multiplier)

        if status:
            self.edit_price_output.setText(f"€ {price:.2f} / pc")
            self.set_message_box("\"Production Cost\" updated.", True)
        else:
            self.set_message_box(message, status)

        return pieces, multiplier, total_cost, price

    def save_product_costing(self):
        product = self.edit_product_dropdown.currentText()
        pieces, multiplier, total_cost, price = self.calculate_total_cost()

        product_list = []
        for row in range(self.costing_table.rowCount()):
            row_list = []
            ingredient_dropdown = self.costing_table.cellWidget(row, 0)
            ingredient = ingredient_dropdown.currentText()
            row_list.append(ingredient)
            amount_input = self.costing_table.cellWidget(row, 1)
            amount = amount_input.text()
            row_list.append(amount)
            unit_dropdown = self.costing_table.cellWidget(row, 2)
            unit = unit_dropdown.currentText()
            row_list.append(unit)
            line_cost = self.calculate_cost_table_row(row)
            row_list.append(line_cost)
            product_list.append(row_list)

        message, status = self.main.save_product_costing(product, pieces, multiplier, total_cost, price, product_list)

        self.set_message_box(message, status)

class TablePopup(QDialog):
    def __init__(self, product_name, parent=None):
        super().__init__(parent)

        self.main = AppMain()

        self.setWindowTitle(f"Product Details - {product_name}")
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel(f"Ingredients for: {product_name}")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.load_product_data(product_name)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("padding: 5px;")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def load_product_data(self, product_name):
        try:
            df = self.main.get_product_dataframe(product_name)

            if df.empty:
                self.table.setRowCount(1)
                self.table.setColumnCount(1)
                self.table.setItem(0, 0, QTableWidgetItem("No data available"))
                return

            self.table.setRowCount(len(df))
            self.table.setColumnCount(len(df.columns))

            self.table.setHorizontalHeaderLabels(df.columns.tolist())

            for row_idx in range(len(df)):
                for col_idx in range(len(df.columns)):
                    value = str(df.iloc[row_idx, col_idx])
                    item = QTableWidgetItem(value)
                    self.table.setItem(row_idx, col_idx, item)

            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except FileNotFoundError:
            self.table.setRowCount(1)
            self.table.setColumnCount(1)
            self.table.setItem(0, 0, QTableWidgetItem(f"File not found for {product_name}"))
        except Exception as e:
            self.table.setRowCount(1)
            self.table.setColumnCount(1)
            self.table.setItem(0, 0, QTableWidgetItem(f"Error loading data: {str(e)}"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppGUI()
    window.show()
    sys.exit(app.exec())