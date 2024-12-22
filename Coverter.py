import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QComboBox, QTextEdit
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

class CurrencyConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Конвертер валют')
        self.setGeometry(100, 100, 400, 500)

        self.api_url = 'https://api.exchangerate-api.com/v4/latest/USD'
        self.conversion_history = []

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText('Введіть суму')
        self.amount_input.setStyleSheet(self.get_input_style())
        self.amount_input.setGraphicsEffect(self.get_effect())
        layout.addWidget(self.amount_input)

        self.from_currency = QComboBox(self)
        self.to_currency = QComboBox(self)
        self.populate_currencies()
        self.from_currency.setStyleSheet(self.get_combo_style())
        self.to_currency.setStyleSheet(self.get_combo_style())
        layout.addWidget(self.from_currency)
        layout.addWidget(self.to_currency)

        self.convert_button = QPushButton('Конвертувати', self)
        self.convert_button.setStyleSheet(self.get_button_style())
        self.convert_button.setGraphicsEffect(self.get_effect())
        self.convert_button.clicked.connect(self.convert_currency)
        layout.addWidget(self.convert_button)

        self.result_label = QLabel('', self)
        self.result_label.setStyleSheet(self.get_result_style())
        layout.addWidget(self.result_label)

        self.history_display = QTextEdit(self)
        self.history_display.setReadOnly(True)
        self.history_display.setStyleSheet(self.get_history_style())
        layout.addWidget(self.history_display)

        self.theme_switch = QPushButton('Перемкнути тему', self)
        self.theme_switch.setStyleSheet(self.get_button_style())
        self.theme_switch.setGraphicsEffect(self.get_effect())
        self.theme_switch.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_switch)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.is_dark_theme = False
        self.apply_theme()

    def get_input_style(self):
        return (
            "font-size: 16px; padding: 10px; border-radius: 10px; border: 1px solid #ccc;"
            "background-color: #fff; color: #333;"
        )

    def get_combo_style(self):
        return (
            "font-size: 16px; padding: 10px; border-radius: 10px; border: 1px solid #ccc;"
            "background-color: #fff; color: #333;"
        )

    def get_button_style_dark(self):
        return (
            "font-size: 16px; padding: 10px; background-color: #4a7ac2; color: white; "
            "border: none; border-radius: 10px; transition: background-color 0.3s;"
        )
    
    def get_button_style(self):
        return (
            "font-size: 16px; padding: 10px; background-color: #4CAF50; color: white; "
            "border: none; border-radius: 10px; transition: background-color 0.3s;"
        )

    def get_result_style(self):
        return "font-size: 18px; font-weight: bold; padding: 10px;"

    def get_history_style(self):
        return (
            "font-size: 14px; padding: 10px; background-color: #f9f9f9; border: 1px solid #ccc; "
            "border-radius: 10px; color: #333;"
        )

    def get_effect(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 100))
        return shadow

    def apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet(
                "background-color: #333; color: #f4f4f4;"
                "QLineEdit { background-color: #555; color: #f4f4f4; }"
                "QComboBox { background-color: #555; color: #f4f4f4; }"
                "QPushButton { background-color: #4CAF50; color: white; }"
                "QLabel { color: #f4f4f4; }"
                "QTextEdit { background-color: #444; color: #f4f4f4; }"
            )
            self.convert_button.setStyleSheet(self.get_button_style_dark())
            self.theme_switch.setStyleSheet(self.get_button_style_dark()) 
        else:
            self.setStyleSheet(
                "background-color: #f4f4f4; color: #333;"
                "QLineEdit { background-color: white; color: #333; }"
                "QComboBox { background-color: white; color: #333; }"
                "QPushButton { background-color: #4CAF50; color: white; }"
                "QLabel { color: #333; }"
                "QTextEdit { background-color: #f9f9f9; color: #333; }"
            )
            self.convert_button.setStyleSheet(self.get_button_style())
            self.theme_switch.setStyleSheet(self.get_button_style()) 

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def populate_currencies(self):
        response = requests.get(self.api_url)
        data = response.json()
        self.currencies = data['rates']

        self.from_currency.addItems(self.currencies.keys())
        self.to_currency.addItems(self.currencies.keys())

    def convert_currency(self):
        try:
            amount = float(self.amount_input.text())
            from_currency = self.from_currency.currentText()
            to_currency = self.to_currency.currentText()

            if from_currency == to_currency:
                self.result_label.setText(f'Результат: {amount:.2f} {to_currency}')
                return

            response = requests.get(self.api_url)
            data = response.json()
            rates = data['rates']

            base_amount = amount / rates[from_currency]
            converted_amount = base_amount * rates[to_currency]

            result = f'{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}'
            self.result_label.setText(f'Результат: {converted_amount:.2f} {to_currency}')

            self.conversion_history.append(result)
            self.update_history_display()

        except ValueError:
            self.result_label.setText('Будь ласка, введіть правильну суму.')

    def update_history_display(self):
        history_text = "\n".join(self.conversion_history)
        self.history_display.setText(history_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CurrencyConverter()
    window.show()
    sys.exit(app.exec_())
