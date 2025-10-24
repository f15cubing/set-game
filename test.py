# Test which implementation of is_set is better
# is_set_1 checks if each characteristic adds up to 0 mod 3
# is_set_2 checks if there are 1 or 3 distinct values
# is_set_1 is marginally faster, averaging 0.022 seconds over all possible combinations of 3 cards
# is_set_2 averaged 0.030 seconds over all combinations

import time
import random
from itertools import combinations

def test_speed():
    deck = [(a,b,c,d) for a in range(3) for b in range(3) for c in range(3) for d in range(3)]
    random.shuffle(deck)
    table = deck[:81]

    start_time = time.perf_counter()

    # Check for SET
    counter = 0
    for c1,c2,c3 in combinations(table, 3):
        if is_set_2(c1,c2,c3):
            counter += 1

    end_time = time.perf_counter()

    execution_time = end_time - start_time
    return execution_time

def is_set_1(c1, c2, c3):
    """Check if 3 cards form a valid set."""
    for i in range(4):
        if (c1[i] + c2[i] + c3[i]) % 3 != 0:
            return False
    return True

def is_set_2(c1, c2, c3):
    """Check if 3 cards form a valid set."""
    for i in range(4):
        vals = {c1[i], c2[i], c3[i]}
        if len(vals) == 2:
            return False
    return True


times = []
for i in range(1000):
    new_time = test_speed()
    times.append(new_time)
print(sum(times) / len(times))
