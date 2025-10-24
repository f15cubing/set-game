import random
from itertools import combinations

def create_deck():
    """Create a shuffled 81-card SET deck."""
    deck = [(shape, color, shade, number)
            for shape in range(3)
            for color in range(3)
            for shade in range(3)
            for number in range(3)]
    random.shuffle(deck)
    return deck

def is_set(c1, c2, c3):
    """Check if 3 cards form a valid set."""
    for i in range(4):
        if (c1[i] + c2[i] + c3[i]) % 3 != 0: # Marginally faster than checking if the set has 1 or 3 items
            return False
    return True

def exists_set(table):
    """Check if a set exists in a given collection of cards"""
    for c1,c2,c3 in combinations(table, 3):
        if is_set(c1,c2,c3):
            return True
    return False
