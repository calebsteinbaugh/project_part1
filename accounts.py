
class Account:
    """
    A class representing a bank account with deposit and withdrawal functionality.
    
    Attributes:
        __name: The account holder's name
        __balance: The current account balance
        __username: The account username
        __password: The account password
    """
    
    def __init__(self, name: str, username: str, password: str, balance: float = 0) -> None:
        """
        Initialize a new Account instance.
        
        Args:
            name: The account holder's name
            username: The account username (must be alphanumeric)
            password: The account password (must be alphanumeric)
            balance: The initial balance (default is 0)
        
        Raises:
            ValueError: If username or password don't meet requirements
        """
        self.__name: str = name
        self.__balance: float = 0
        self.__username: str = ''
        self.__password: str = ''
        
        self.set_username(username)
        self.set_password(password)
        self.set_balance(balance)
        
    def set_balance(self, value: float) -> None:
        """
        Set the account balance.
        
        Args:
            value: The balance to set (negative values default to 0)
        """
        if value < 0:
            self.__balance = 0
        else:
            self.__balance = value
            
    def set_username(self, username: str) -> None:
        """
        Set the account username.
        
        Args:
            username: The username to set
        
        Raises:
            ValueError: If username is less than 1 character or not alphanumeric
        """
        if len(username) < 1 or not username.isalnum():
            raise ValueError(r"Username must be at least 1 character and alphanumeric")
        
        self.__username = username
        
    def set_password(self, password: str) -> None:
        """
        Set the account password.
        
        Args:
            password: The password to set
        
        Raises:
            ValueError: If password is less than 1 character or not alphanumeric
        """
        if len(password) < 1 or not password.isalnum():
            raise ValueError(r"Password must be at least 1 character and alphanumeric")
        
        self.__password = password
            
    def deposit(self, amount: float) -> bool:
        """
        Deposit funds into the account.
        
        Args:
            amount: The amount to deposit
        
        Returns:
            True if deposit was successful, False otherwise
        """
        if amount > 0:
            self.set_balance(self.get_balance() + amount)
            return True
        return False
     
    def withdraw(self, amount: float) -> bool:
        """
        Withdraw funds from the account.
        
        Args:
            amount: The amount to withdraw
        
        Returns:
            True if withdrawal was successful, False otherwise
        """
        if amount > 0 and amount <= self.get_balance():
            self.set_balance(self.get_balance() - amount)
            return True
        return False
     
    def get_balance(self) -> float:
        """
        Get the current account balance.
        
        Returns:
            The current balance
        """
        return self.__balance
     
    def get_name(self) -> str:
        """
        Get the account holder's name.
        
        Returns:
            The account holder's name
        """
        return self.__name

    def get_username(self) -> str:
        """
        Get the account username.
        
        Returns:
            The account username
        """
        return self.__username
     
    def get_password(self) -> str:
        """
        Get the account password.
        
        Returns:
            The account password
        """
        return self.__password
     
    def set_name(self, value: str) -> None:
        """
        Set the account holder's name.
        
        Args:
            value: The name to set
        """
        self.__name = value
         
    def __str__(self) -> str:
        """
        Return a string representation of the account.
        
        Returns:
            A formatted string with account name and balance
        """
        return f'Account name: {self.get_name()}, Account balance: {self.get_balance():.2f}'


class SavingAccount(Account):
    """
    A savings account class that extends Account with interest and deposit tracking.
    
    Attributes:
        minimum: The minimum balance required (default is 100)
        rate: The interest rate applied (default is 0.02 or 2%)
        __deposit_count: Counter for number of deposits made
    """
    
    minimum: float = 100
    rate: float = 0.02
         
    def __init__(self, name: str, username: str, password: str, balance: float = minimum, deposit_count: int = 0) -> None:
        """
        Initialize a new SavingAccount instance.
        
        Args:
            name: The account holder's name
            username: The account username
            password: The account password
            balance: The initial balance (default is minimum)
            deposit_count: The initial deposit count (default is 0)
        """
        super().__init__(name, username, password, balance)
        self.__deposit_count: int = deposit_count
     
    def apply_interest(self) -> None:
        """
        Apply interest to the savings account based on current balance.
        """
        interest: float = self.get_balance() * self.rate
        super().deposit(interest)
        
    def deposit(self, amount: float) -> bool:
        """
        Deposit funds into the savings account.
        
        Args:
            amount: The amount to deposit
        
        Returns:
            True if deposit was successful, False otherwise
        """
        if amount <= 0:
            return False
        if super().deposit(amount):
            self.__deposit_count += 1
             
            if self.__deposit_count % 5 == 0:
                self.apply_interest()
            return True
     
        return False
     
    def withdraw(self, amount: float) -> bool:
        """
        Withdraw funds from the savings account.
        
        Args:
            amount: The amount to withdraw
        
        Returns:
            True if withdrawal was successful, False otherwise
        """
        if amount <= 0 or (super().get_balance() - amount) < self.minimum:
            return False
        return super().withdraw(amount)
         
    def set_balance(self, value: float) -> None:
        """
        Set the savings account balance ensuring minimum is maintained.
        
        Args:
            value: The balance to set
        """
        if value < self.minimum:
            super().set_balance(self.minimum)
        else:
            super().set_balance(value)
     
    def __str__(self) -> str:
        """
        Return a string representation of the savings account.
        
        Returns:
            A formatted string with account information
        """
        return f'{super().__str__()}'
