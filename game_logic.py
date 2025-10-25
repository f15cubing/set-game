import random
import math
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
    count = 0
    for c1,c2,c3 in combinations(table, 3):
        if is_set(c1,c2,c3):
            count += 1
    return count

def calculate_score(raw_score):
    """Calculate score given time, number of sets, and penalty points"""
    time = raw_score["time"]
    sets_found = raw_score["sets"]
    penalty = raw_score["penalty"]

    if sets_found < 21:
        # In this case, at least 21 cards are left in the deck, and there exists at least one set
        sets_found = 0
    elif sets_found > 23:
        sets_found = sets_found**2

    score = sets_found**0.55 * (1000 / time) - 5*penalty
    score = round(score, 1)
    return score
