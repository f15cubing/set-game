# SET — The Card Game (Python)

A graphical implementation of the classic **SET** card game, built with **Python** and **Tkinter**, organized into modular files for clarity and extensibility.

---

## Features

- **81-card deck** — 3 shapes × 3 colors × 3 shadings × 3 numbers
- **Interactive gameplay** — click to select cards, automatically checks for valid sets
- **Dynamic layout** — adapts to any number of cards with a centered 3×n grid
- **Smart replacement logic** — replaces cards when ≤12 on the table, removes them otherwise
- **New deck button** — start a fresh game while keeping previously found sets
- Tracks the number of sets found and cards remaining in the deck
- **Timed runs** — see how long it takes you to finish a complete deck

---

## How to Play

Each card has **four attributes**:

| Attribute | Options |
|------------|----------|
| Shape | Oval, Diamond, Squiggle |
| Color | Red, Green, Purple |
| Shading | Solid, Striped, Empty |
| Number | One, Two, or Three symbols |

A **SET** consists of **3 cards** where, for *each attribute*, the values are either **all the same** or **all different**.

Click three cards — if they form a valid SET, they disappear (and new ones are dealt).

---

## How to Run

### Requirements
- **Python 3.9+**
- **Tkinter**

### Run the game

```bash
python main.py
