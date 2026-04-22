from PyQt6.QtWidgets import QMainWindow
from accounts import Account, SavingAccount
from banking_info_gui import Ui_banking_info_window
import csv


class LoginController:
    """
    Controller class for handling user login and banking transactions.
    
    Manages login authentication and creates/updates banking GUI windows with
    account balance information. Handles deposit and withdrawal transactions
    for both checking and savings accounts.
    """
    
    def __init__(self, ui: object, window: QMainWindow) -> None:
        """
        Initialize the LoginController with UI and window references.
        
        Args:
            ui (object): The login window UI object containing input fields and buttons.
            window (QMainWindow): The main window reference for the login screen.
            
        Returns:
            None
        """
        self.ui: object = ui
        self.window: QMainWindow = window

        self.valid_username: str = "caleb"
        self.valid_password: str = "1234"
        
        self.checking: Account | None = None
        self.savings: SavingAccount | None = None
        self.banking_window: QMainWindow | None = None
        self.banking_ui: Ui_banking_info_window | None = None

        self.connect_signals()
        self.ui.feedback_txt.setText("")

    def connect_signals(self) -> None:
        """
        Connect UI signals to their corresponding slot methods.
        
        Specifically connects the signin button to the login method.
        
        Returns:
            None
        """
        self.ui.signin_button.clicked.connect(self.login)

    def login(self) -> None:
        """
        Authenticate user credentials and initialize banking window on successful login.
        
        Validates that username and password fields are not empty, checks credentials
        against valid credentials, and creates/displays the banking interface with
        account objects upon successful authentication.
        
        Returns:
            None
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

    def transaction(self) -> None:
        """
        Process banking transactions (deposits and withdrawals).
        
        Validates transaction amount, determines transaction type (deposit/withdraw),
        selects target account (checking/savings), and updates account balances
        and UI labels accordingly. Provides validation feedback for invalid inputs.
        
        Returns:
            None
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