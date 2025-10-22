import random

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
        vals = {c1[i], c2[i], c3[i]}
        if len(vals) == 2:
            return False
    return True
