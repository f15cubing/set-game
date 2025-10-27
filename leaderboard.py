import json
import os

LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    """Load leaderboard from file safely — handles empty or corrupted files."""
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            data = f.read().strip()
            if not data:
                return []  # empty file
            return json.loads(data)
    except (json.JSONDecodeError, ValueError):
        # Corrupted file → reset to empty leaderboard
        return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=2)
