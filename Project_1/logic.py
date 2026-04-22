from PyQt6.QtWidgets import QMainWindow
from accounts import Account, SavingAccount
from banking_info_gui import Ui_banking_info_window
import csv


class LoginController:
    def __init__(self, ui, window):
        self.ui = ui
        self.window = window

        self.valid_username = "caleb"
        self.valid_password = "1234"

        self.connect_signals()
        self.ui.feedback_txt.setText("")

    def connect_signals(self):
        self.ui.signin_button.clicked.connect(self.login)

    def login(self):
        username = self.ui.username_input.text().strip()
        password = self.ui.password_input.text().strip()

        if username == "":
            self.ui.feedback_txt.setText(
                "Please enter a username.\nUsername must be alphanumeric and\n>8 characters."
            )
            return

        if password == "":
            self.ui.feedback_txt.setText(
                "Please enter a password.\nPassword must be alphanumeric and\n>4 characters."
            )
            return

        if username == self.valid_username and password == self.valid_password:
            self.ui.feedback_txt.setText("Login successful.")

            # Create account objects
            self.checking = Account(username, username, password, 1000)
            self.savings = SavingAccount(username, username, password, 500)

            # Create banking window
            self.banking_window = QMainWindow()
            self.banking_ui = Ui_banking_info_window()
            self.banking_ui.setupUi(self.banking_window)

            # Fill banking window
            self.banking_ui.person_name_label.setText(username)
            self.banking_ui.checking_balance_label.setText("$1000.00")
            self.banking_ui.savings_balance_label.setText("$500.00")
            self.banking_ui.validation_message_txt.setText("")

            # Connect submit button
            self.banking_ui.submit_trans_button.clicked.connect(self.transaction)

            self.banking_window.show()
            self.window.close()

        else:
            self.ui.feedback_txt.setText("Invalid username or password.")

    def transaction(self):
        try:
            amount = float(self.banking_ui.amount_input.text().strip())
        except ValueError:
            self.banking_ui.validation_message_txt.setText("Enter a valid amount.")
            return

        if amount <= 0:
            self.banking_ui.validation_message_txt.setText("Amount must be positive.")
            return

        # Deposit
        if self.banking_ui.deposit_button.isChecked():
            if self.banking_ui.checking_button.isChecked():
                self.checking.deposit(amount)
                self.banking_ui.validation_message_txt.setText(
                    "Deposit to checking successful."
                )

            elif self.banking_ui.savings_button.isChecked():
                self.savings.deposit(amount)
                self.banking_ui.validation_message_txt.setText(
                    "Deposit to savings successful."
                )

            else:
                self.banking_ui.validation_message_txt.setText(
                    "Select an account to deposit into."
                )
                return

        # Withdraw
        elif self.banking_ui.withdraw_button.isChecked():
            if self.banking_ui.checking_button.isChecked():
                if self.checking.withdraw(amount):
                    self.banking_ui.validation_message_txt.setText(
                        "Withdraw from checking successful."
                    )
                else:
                    self.banking_ui.validation_message_txt.setText(
                        "Insufficient funds for withdrawal."
                    )
                    return

            elif self.banking_ui.savings_button.isChecked():
                if self.savings.withdraw(amount):
                    self.banking_ui.validation_message_txt.setText(
                        "Withdraw from savings successful."
                    )
                else:
                    self.banking_ui.validation_message_txt.setText(
                        "Insufficient funds."
                    )
                    return

            else:
                self.banking_ui.validation_message_txt.setText(
                    "Select an account to withdraw from."
                )
                return

        else:
            self.banking_ui.validation_message_txt.setText(
                "Select deposit or withdraw."
            )
            return

        # Update balance labels
        self.banking_ui.user_checking_balance_label.setText(
            f"${self.checking.get_balance():.2f}"
        )
        self.banking_ui.user_savings_balance_label.setText(
            f"${self.savings.get_balance():.2f}"
        )

        self.banking_ui.amount_input.clear()