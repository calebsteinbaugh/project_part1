from PyQt6.QtWidgets import QMainWindow
from accounts import Account, SavingAccount
from banking_info_gui import Ui_banking_info_window
import csv

'''
Code was reformated by Copilot to increase readability
'''
class LoginController:
    """
    Controller class handles login logic,
    initializing account objects, managing the banking UI,
    and processing transactions.
    """

    def __init__(self, ui, window) -> None:
        """
        Initialize the login controller.

        Args:
            ui: The UI object for the login window.
            window: The main QMainWindow for the login interface.
        """
        self.ui = ui
        self.window = window

        self.valid_username: str = "caleb"
        self.valid_password: str = "1234"

        self.connect_signals()
        self.ui.feedback_txt.setText("")

    def connect_signals(self) -> None:
        """
        Connect UI signals to their corresponding slots.
        """
        self.ui.signin_button.clicked.connect(self.login)

    def login(self) -> None:
        """
        Handle user login. Validates input and, if successful,
        initializes account objects and opens the banking window.
        """
        username: str = self.ui.username_input.text().strip()
        password: str = self.ui.password_input.text().strip()

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
            self.checking: Account = Account(username, username, password, 1000)
            self.savings: SavingAccount = SavingAccount(username, username, password, 500)

            # Create banking window
            self.banking_window: QMainWindow = QMainWindow()
            self.banking_ui: Ui_banking_info_window = Ui_banking_info_window()
            self.banking_ui.setupUi(self.banking_window)

            # Populate UI
            self.banking_ui.person_name_label.setText(username)
            self.banking_ui.user_checking_balance_label.setText("$1000.00")
            self.banking_ui.user_savings_balance_label.setText("$500.00")
            self.banking_ui.validation_message_txt.setText("")

            # Connect transaction button
            self.banking_ui.submit_trans_button.clicked.connect(self.transaction)

            self.banking_window.show()
            self.window.close()

        else:
            self.ui.feedback_txt.setText("Invalid username or password.")

    def transaction(self) -> None:
        """
        Process a deposit or withdrawal transaction based on user input.
        Updates account balances and logs the transaction.
        """
        try:
            amount: float = float(self.banking_ui.amount_input.text().strip())
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
                self.store_transaction(
                    self.checking.get_username(),
                    "Deposit",
                    "Checking",
                    amount,
                    self.checking.get_balance(),
                )
                self.banking_ui.validation_message_txt.setText(
                    "Deposit to checking successful."
                )

            elif self.banking_ui.savings_button.isChecked():
                self.savings.deposit(amount)
                self.store_transaction(
                    self.savings.get_username(),
                    "Deposit",
                    "Savings",
                    amount,
                    self.savings.get_balance(),
                )
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
                    self.store_transaction(
                        self.checking.get_username(),
                        "Withdraw",
                        "Checking",
                        amount,
                        self.checking.get_balance(),
                    )
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
                    self.store_transaction(
                        self.savings.get_username(),
                        "Withdraw",
                        "Savings",
                        amount,
                        self.savings.get_balance(),
                    )
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

        # Update balances
        self.banking_ui.user_checking_balance_label.setText(
            f"${self.checking.get_balance():.2f}"
        )
        self.banking_ui.user_savings_balance_label.setText(
            f"${self.savings.get_balance():.2f}"
        )

        self.banking_ui.amount_input.clear()

    def store_transaction(
        self,
        username: str,
        action: str,
        account_type: str,
        amount: float,
        balance: float,
    ) -> None:
        """
        Store a transaction record in a CSV file.

        Args:
            username (str): Username associated with the transaction.
            action (str): Type of transaction ("Deposit" or "Withdraw").
            account_type (str): Account type ("Checking" or "Savings").
            amount (float): Transaction amount.
            balance (float): Resulting account balance after transaction.
        """
        with open("transactions.csv", "a", newline="") as transactions_file:
            writer = csv.writer(transactions_file)
            writer.writerow([username, action, account_type, amount, balance])
