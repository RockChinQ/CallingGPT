# examples/random.py
from random import choice

def choose_randomly(l: list[str]) -> str:
    """Choose a random element from a list.

    Args:
        l: The list to choose from.

    Returns:
        The chosen element.
    """
    return choice(l)

__functions__ = [choose_randomly]