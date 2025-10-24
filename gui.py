import tkinter as tk
from game_logic import create_deck, is_set
from shapes import draw_card
import time

class SetCardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("SET Game")
        self.root.configure(bg="#2c3e50")

        # Palette
        self.colors = ['#d63031', '#00b894', '#6c5ce7']

        # Game state
        self.deck = create_deck()
        self.table = [self.deck.pop() for _ in range(12)]
        self.selected = []
        self.collected_sets = []

        # Timed-run state
        self.timed_run_active = False
        self.run_start_time = 0.0
        self.run_elapsed = 0.0
        self.timer_update_job = None


        # Layout setup
        self.frame = tk.Frame(root, bg="#2c3e50")
        self.frame.pack(padx=20, pady=20)

        self.info_frame = tk.Frame(root, bg="#2c3e50")
        self.info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # How many sets have been found label
        self.sets_label = tk.Label(self.info_frame, text="Sets Found: 0",
                                   bg="#2c3e50", fg="white", font=("Arial", 16))
        self.sets_label.pack(side=tk.LEFT, padx=10)

        # Cards left in deck label
        self.deck_label = tk.Label(self.info_frame, text=f"Cards left: {len(self.deck)}",
                                   bg="#2c3e50", fg="white", font=("Arial", 16))
        self.deck_label.pack(side=tk.RIGHT, padx=10)

        # Add 3 new cards button
        self.add_cards_button = tk.Button(self.info_frame, text="Add 3 Cards",
                            font=("Arial", 14), bg="#e67e22", fg="white",
                            command=self.add_three_cards)
        self.add_cards_button.pack(side=tk.RIGHT, padx=10)

        # New deck button
        self.new_deck_button = tk.Button(self.info_frame, text="New Deck",
                            font=("Arial", 14), bg="#3498db", fg="white",
                            command=self.new_deck)
        self.new_deck_button.pack(side=tk.RIGHT, padx=10)

        # Start Timed Run Button
        self.start_run_button = tk.Button(self.info_frame, text="Start Timed Run",
                                          font=("Arial", 14), bg="#2ecc71", fg="white",
                                          command=self.start_timed_run)
        self.start_run_button.pack(side=tk.RIGHT, padx=10)

        # End Run button (disabled until run is active)
        self.end_run_button = tk.Button(self.info_frame, text="End Run",
                                        font=("Arial", 14), bg="#e74c3c", fg="white",
                                        command=self.end_timed_run, state=tk.DISABLED)
        self.end_run_button.pack(side=tk.RIGHT, padx=10)

        self.draw_table()

    def draw_table(self):
        """Display cards on board"""
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
        """Allow user to select a card"""
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

    def start_timed_run(self):
        pass
        #self.new_deck()
        #start_time = time.time()

    def end_timed_run(self):
        pass
