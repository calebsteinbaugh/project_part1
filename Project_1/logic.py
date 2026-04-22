def example_method(param1: int, param2: str) -> None:
    """
    Example method that does something.

    Args:
        param1 (int): An integer parameter.
        param2 (str): A string parameter.
    """
    pass

class ExampleClass:
    """
    An example class with methods demonstrating docstrings and type hints.
    """
    def __init__(self, name: str) -> None:
        """
        Initialize the example class.

        Args:
            name (str): The name of the example.
        """
        self.name = name

    def display_name(self) -> None:
        """
        Display the name of the example.
        """  
        print(self.name)