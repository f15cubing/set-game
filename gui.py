import tkinter as tk
from game_logic import create_deck, is_set, exists_set, calculate_score
from shapes import draw_card
import time
from tkinter import messagebox

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
        self.score = 0
        self.raw_score = {"sets" : 0, "time" : 0, "penalty": 0}


        # Layout setup
        self.frame = tk.Frame(root, bg="#2c3e50")
        self.frame.pack(padx=20, pady=20)

        self.info_frame = tk.Frame(root, bg="#2c3e50")
        self.info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Score label
        self.score_label = tk.Label(
            self.root,
            text=f"Score: {self.score}",
            font=("Arial", 16),
            bg="#47bbc1",
            fg="white"
        )
        self.score_label.place(x=20, y=10)


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

        # Timer
        self.timer_label = tk.Label(self.info_frame, text="Time: 00:00.00",
                                    bg="#2c3e50", fg="white", font=("Arial", 16))
        self.timer_label.pack(side=tk.LEFT, padx=10)

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

                if self.timed_run_active:
                    self.raw_score["sets"] += 1

                if len(self.table) <= 12:
                    self.replace_cards(self.selected)
                else:
                    self.remove_selected_cards(self.selected)

                if self.timed_run_active and not exists_set(self.table) and not self.deck:
                    # Stop automatically (Deck is finished and no more sets remain)
                    # pass manual=False to indicate automatic completion
                    self.end_timed_run(manual=False)

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
        """Add 3 cards to the table"""
        if not self.deck:
            tk.messagebox.showwarning("No more cards", "The deck is empty!")
            return

        # Check how 'efficient' adding new cards was
        if self.timed_run_active:
            self.raw_score["penalty"] += exists_set(self.table)

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
        """Start a timed run: disable New Deck, enable End Run, start timer."""
        if self.timed_run_active:
            return

        # Set data for beginning of run
        self.collected_sets = []
        self.sets_label.config(text=f"Sets Found: {len(self.collected_sets)}")
        self.timed_run_active = True
        self.run_start_time = time.perf_counter()
        self.run_elapsed = 0.0
        self.score = 0


        # UI updates
        self.new_deck_button.config(state=tk.DISABLED)   # disable New Deck during run
        self.start_run_button.config(state=tk.DISABLED)
        self.end_run_button.config(state=tk.NORMAL)
        self.new_deck() # Ensure a new deck is drawn for the timed run

        # Start timer loop
        if self.timer_update_job:
            self.root.after_cancel(self.timer_update_job)
            self.timer_update_job = None
        self.update_timer()

    def end_timed_run(self, manual = True):
        """
        End the timed run. If manual=True, user clicked End Run;
        otherwise it's automatic (deck finished).
        """
        if not self.timed_run_active:
            return

        self.timed_run_active = False

        # cancel scheduled update if any
        if self.timer_update_job:
            self.root.after_cancel(self.timer_update_job)
            self.timer_update_job = None

        # final elapsed
        final_elapsed = time.perf_counter() - self.run_start_time
        self.raw_score["time"] = final_elapsed
        final_time_str = self.format_time(final_elapsed)


        # re-enable UI
        self.new_deck_button.config(state=tk.NORMAL)
        self.start_run_button.config(state=tk.NORMAL)
        self.end_run_button.config(state=tk.DISABLED)

        # Show final score & time in a dialog
        sets_found = len(self.collected_sets)
        if manual:
            title = "Timed Run Ended"
        else:
            title = "Timed Run Complete"

        self.score = calculate_score(self.raw_score)

        tk.messagebox.showinfo(title, f"Run finished!\n\nSets found: {sets_found}\nTime: {final_time_str}\nScore: {self.score}")

        # update timer and socre label to final time
        self.timer_label.config(text=f"Time: {final_time_str}")
        self.score_label.config(text=f"Score: {self.score}")


        for x in self.raw_score:
            self.raw_score[x] = 0

    def format_time(self, seconds):
        """Return MM:SS.ss string."""
        mins = int(seconds // 60)
        secs = seconds - mins * 60
        return f"{mins:02d}:{secs:05.2f}"

    def update_timer(self):
        """Update timer label; scheduled using after while run active."""
        if not self.timed_run_active:
            return

        now = time.perf_counter()
        self.run_elapsed = now - self.run_start_time
        self.timer_label.config(text=f"Time: {self.format_time(self.run_elapsed)}")

        # schedule next update (50 ms)
        self.timer_update_job = self.root.after(50, self.update_timer)
