"""Simple calculator tools for the hello_world agent."""


def add(a: float, b: float) -> dict:
    """Adds two numbers together.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        A dict with the sum result.
    """
    return {"result": a + b}


def subtract(a: float, b: float) -> dict:
    """Subtracts two numbers.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        A dict with the difference result.
    """
    return {"result": a - b}


def multiply(a: float, b: float) -> dict:
    """Multiplies two numbers together.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        A dict with the product result.
    """
    return {"result": a * b}
