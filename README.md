# set-game
# SET — The Card Game (Python)

A graphical implementation of the classic **SET** card game built in **Python** using `tkinter`.

---

## Features

- Full 81-card deck (3 shapes × 3 colors × 3 fills × 3 numbers)
- Click to select cards — automatically checks if a set is formed
- Cards that form a SET are replaced (or removed if more than 12)
- Centered 3×n grid layout

---

## How to Play

Each card has **four attributes**:
- **Shape:** oval, diamond, or squiggle
- **Color:** red, green, or purple
- **Shading:** solid, striped, or empty
- **Number:** one, two, or three symbols

A **SET** consists of 3 cards where, for *each attribute*,
the values are either **all the same** or **all different**.

Click any three cards — if they form a valid set, they are removed and replaced.

---

## 🚀 How to Run

### Requirements
- Python 3.9+
- Tkinter (included with most Python installations)

### Run the game
```bash
python set_game.py
