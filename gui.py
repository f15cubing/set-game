import tkinter as tk
from game_logic import create_deck, is_set
from shapes import draw_card

class SetCardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("SET Game")
        self.root.configure(bg="#2c3e50")

        self.colors = ['#d63031', '#00b894', '#6c5ce7']
        self.deck = create_deck()
        self.table = [self.deck.pop() for _ in range(12)]
        self.selected = []
        self.collected_sets = []

        # Layout setup
        self.frame = tk.Frame(root, bg="#2c3e50")
        self.frame.pack(padx=20, pady=20)

        self.info_frame = tk.Frame(root, bg="#2c3e50")
        self.info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.sets_label = tk.Label(self.info_frame, text="Sets Found: 0",
                                   bg="#2c3e50", fg="white", font=("Arial", 16))
        self.sets_label.pack(side=tk.LEFT, padx=10)

        self.deck_label = tk.Label(self.info_frame, text=f"Cards left: {len(self.deck)}",
                                   bg="#2c3e50", fg="white", font=("Arial", 16))
        self.deck_label.pack(side=tk.RIGHT, padx=10)

        self.add_button = tk.Button(self.info_frame, text="Add 3 Cards",
                            font=("Arial", 14), bg="#e67e22", fg="white",
                            command=self.add_three_cards)
        self.add_button.pack(side=tk.RIGHT, padx=10)

        self.new_button = tk.Button(self.info_frame, text="New Deck",
                            font=("Arial", 14), bg="#3498db", fg="white",
                            command=self.new_deck)
        self.new_button.pack(side=tk.RIGHT, padx=10)

        self.draw_table()

    def draw_table(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        num_cards = len(self.table)
        cols = (num_cards + 2) // 3

        for i, card in enumerate(self.table):
            r, c = divmod(i, cols)
            canvas = tk.Canvas(self.frame, width=110, height=150, bg="white",
                               borderwidth=0, highlightthickness=3,
                               highlightbackground="#bdc3c7")
            canvas.grid(row=r, column=c, padx=8, pady=8)
            canvas.bind("<Button-1>", lambda e, idx=i: self.select_card(idx))
            draw_card(canvas, card, self.colors)

    def select_card(self, idx):
        if idx in self.selected:
            self.selected.remove(idx)
        else:
            self.selected.append(idx)
        self.update_highlight()

        if len(self.selected) == 3:
            c1, c2, c3 = [self.table[i] for i in self.selected]
            if is_set(c1, c2, c3):
                self.collected_sets.append(tuple(sorted([c1, c2, c3])))
                self.sets_label.config(text=f"Sets Found: {len(self.collected_sets)}")

                if len(self.table) <= 12:
                    self.replace_cards(self.selected)
                else:
                    self.remove_selected_cards(self.selected)
            self.selected.clear()
            self.update_highlight()

    def update_highlight(self):
        for i, canvas in enumerate(self.frame.winfo_children()):
            canvas.configure(highlightbackground="#f1c40f" if i in self.selected else "#bdc3c7")

    def replace_cards(self, indices):
        indices.sort(reverse=True)
        for idx in indices:
            if self.deck:
                self.table[idx] = self.deck.pop()
            else:
                del self.table[idx]
        self.deck_label.config(text=f"Deck: {len(self.deck)}")
        self.draw_table()

    def remove_selected_cards(self, indices):
        indices.sort(reverse=True)
        for idx in indices:
            del self.table[idx]
        self.draw_table()

    def add_three_cards(self):
        if not self.deck:
            tk.messagebox.showwarning("No more cards", "The deck is empty!")
            return
        for _ in range(3):
            if self.deck:
                self.table.append(self.deck.pop())
        self.deck_label.config(text=f"Deck: {len(self.deck)}")
        self.draw_table()

    def new_deck(self):
        self.deck = create_deck()
        self.table = [self.deck.pop() for _ in range(12)]
        self.selected = []
        self.deck_label.config(text=f"Cards left: {len(self.deck)}")
        self.draw_table()
