import tkinter as tk
import random
import math

class SetCardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("SET Game")
        self.root.configure(bg="#2c3e50")

        self.colors = ['#d63031', '#00b894', '#6c5ce7']
        self.deck = self.create_deck()
        self.table = [self.deck.pop() for _ in range(12)]
        self.selected = []
        self.collected_sets = []

        # Main frame
        self.frame = tk.Frame(root, bg="#2c3e50")
        self.frame.pack(padx=20, pady=20)

        # Info frame
        self.info_frame = tk.Frame(root, bg="#2c3e50")
        self.info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.sets_label = tk.Label(self.info_frame, text="Sets Found: 0",
                                   bg="#2c3e50", fg="white", font=("Arial", 16))
        self.sets_label.pack(side=tk.LEFT, padx=10)

        self.deck_label = tk.Label(self.info_frame, text=f"Deck: {len(self.deck)}",
                                   bg="#2c3e50", fg="white", font=("Arial", 16))
        self.deck_label.pack(side=tk.RIGHT, padx=10)

        self.add_button = tk.Button(self.info_frame, text="Add 3 Cards",
                            font=("Arial", 14), bg="#e67e22", fg="white",
                            command=self.add_three_cards)
        self.add_button.pack(side=tk.RIGHT, padx=10)

        self.draw_table()

    def create_deck(self):
        """
        Create a shuffled 81 card deck.
        """
        deck = [(shape, color, shade, number) for shape in range(3) for color in range(3)
                for shade in range(3) for number in range(3)]
        random.shuffle(deck)
        return deck

    def draw_table(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        num_cards = len(self.table)
        cols = (num_cards + 2) // 3  # 3 rows

        for i, card in enumerate(self.table):
            r, c = divmod(i, cols)
            canvas = tk.Canvas(self.frame, width=110, height=150, bg="white",
                               borderwidth=0, highlightthickness=3,
                               highlightbackground="#bdc3c7")
            canvas.grid(row=r, column=c, padx=8, pady=8)
            canvas.bind("<Button-1>", lambda e, idx=i: self.select_card(idx))
            self.draw_card(canvas, card)

    def select_card(self, idx):
        if idx in self.selected:
            self.selected.remove(idx)
        else:
            self.selected.append(idx)

        self.update_highlight()

        if len(self.selected) == 3:
            c1, c2, c3 = [self.table[i] for i in self.selected]
            if self.is_set(c1, c2, c3):
                self.collected_sets.append(tuple(sorted([c1, c2, c3])))
                self.sets_label.config(text=f"Sets Found: {len(self.collected_sets)}")

                # --- Replacement logic ---
                if len(self.table) <= 12:
                    self.replace_cards(self.selected)
                else:
                    # More than 12 cards: just remove the selected 3
                    self.remove_selected_cards(self.selected)

            self.selected.clear()
            self.update_highlight()

    def update_highlight(self):
        for i, canvas in enumerate(self.frame.winfo_children()):
            if i < len(self.table):
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

    def is_set(self, c1, c2, c3):
        for i in range(4):
            vals = {c1[i], c2[i], c3[i]}
            if len(vals) == 2:
                return False
        return True

    def draw_card(self, canvas, card):
        """
        Render card into interface
        """
        shape, color_idx, shading, number = card
        color = self.colors[color_idx]
        count = number + 1

        spacing = 15
        shape_h = 35
        total_h = count * shape_h + (count-1) * spacing
        start_y = (150 - total_h)/2 + shape_h/2

        for i in range(count):
            y = start_y + i*(shape_h + spacing)
            if shape == 0:
                self.draw_diamond(canvas, 55, y, 40, 18, color, shading)
            elif shape == 1:
                self.draw_oval(canvas, 55, y, 45, 18, color, shading)
            else:
                self.draw_squiggle(canvas, 55, y, 50, 18, color, shading)

    def draw_diamond(self, canvas, x, y, w, h, color, shading):
        """
        Draw diamons centered at (x,y), woth given color and shading.
        """
        pts = [x, y-h, x+w, y, x, y+h, x-w, y]

        if shading == 0:  # Solid
            canvas.create_polygon(pts, fill=color, outline=color, width=2)
        elif shading == 1:  # Striped
            canvas.create_polygon(pts, fill='', outline=color, width=2)  # outline first
            # Draw stripes inside the diamond
            step = 3
            for i in range(-w, w+1, step):
                # compute y-range at this x
                y_top = y - h * (1 - abs(i)/w)
                y_bottom = y + h * (1 - abs(i)/w)
                canvas.create_line(x+i, y_top, x+i, y_bottom, fill=color)
        else:  # Empty
            canvas.create_polygon(pts, fill='', outline=color, width=2)


    def draw_oval(self, canvas, x, y, w, h, color, shading):
        """
        Draw oval centered at (x,y), with given color and shading.
        """
        if shading == 0:  # solid
            canvas.create_oval(x-w, y-h, x+w, y+h, fill=color, outline=color, width=2)
        elif shading == 1:  # striped
            step = 4
            for sx in range(int(x-w), int(x+w), step):
                dx = (sx - x) / w
                if abs(dx) > 1: continue
                dy = (1 - dx*dx)**0.5 * h
                canvas.create_line(sx, y-dy, sx, y+dy, fill=color)
            canvas.create_oval(x-w, y-h, x+w, y+h, outline=color, width=2)  # outline on top
        else:  # empty
            canvas.create_oval(x-w, y-h, x+w, y+h, fill='', outline=color, width=2)


    def draw_squiggle(self, canvas, x, y, w, h, color, shading):
        """
        Draw squiggle centered at (x,y).
        """
        points = [
            x, y - h*0.3,
            x + w*0.3, y - h*1.1,
            x + w*0.8, y - h*0.8,
            x + w, y - h*0.3,
            x + w*0.8, y + h*0.2,
            x + w*0.3, y,
            x, y + h*0.3,
            x - w*0.3, y + h*1.1,
            x - w*0.8, y + h*0.8,
            x - w, y + h*0.3,
            x - w*0.8, y - h*0.2,
            x - w*0.3, y,
        ]
        if shading == 0: # solid
            canvas.create_polygon(points, fill=color, outline=color, width=2, smooth=True)
        elif shading == 1: # striped
            # draw stripes using exact polygon clipping by scanline intersections
            self.draw_striped_polygon(canvas, points, color, step=4)
            canvas.create_polygon(points, fill='', outline=color, width=2, smooth=True)
        else: # empty
            canvas.create_polygon(points, fill='', outline=color, width=2, smooth=True)

    def draw_striped_polygon(self, canvas, points, color, step=4):
        """
        Draw horizontal stripes *only inside* the polygon.
        - points: flat list [x0,y0,x1,y1,...] (polygon should be closed or implicitly closed)
        - color: stripe color
        - step: vertical spacing between stripes in pixels
        """
        # compute vertical bounds
        ys = points[1::2]
        if not ys:
            return
        y_min = math.floor(min(ys))
        y_max = math.ceil(max(ys))

        for y in range(y_min, y_max+1, step):
            xs = self.polygon_scanline_intersections(points, y)
            # pair intersections (xs[0], xs[1]), (xs[2], xs[3]), ...
            # ignore odd point if any (shouldn't happen with well-formed polygon)
            for i in range(0, len(xs)-1, 2):
                x_start = xs[i]
                x_end = xs[i+1]
                canvas.create_line(x_start, y, x_end, y, fill=color)

    def polygon_scanline_intersections(self, points, y):
        """
        Given polygon `points` as a flat list [x0,y0,x1,y1,...],
        return a sorted list of x coordinates where the horizontal
        line at y intersects the polygon edges.

        Uses the standard scanline intersection rule (include lower endpoint,
        exclude upper endpoint) to avoid double-counting vertex intersections.
        Works for non-convex polygons.
        """
        xs = []
        n = len(points) // 2
        for i in range(n):
            x1 = points[2*i]
            y1 = points[2*i + 1]
            x2 = points[2*((i+1) % n)]
            y2 = points[2*((i+1) % n) + 1]

            # Skip horizontal edges entirely
            if y1 == y2:
                continue

            # Determine if scanline y crosses edge (y1..y2)
            # We'll include intersections where y is >= min(y1,y2) and < max(y1,y2)
            y_min = min(y1, y2)
            y_max = max(y1, y2)
            if (y >= y_min) and (y < y_max):
                # compute intersection x
                t = (y - y1) / (y2 - y1)
                xi = x1 + t * (x2 - x1)
                xs.append(xi)

        xs.sort()
        return xs

    def add_three_cards(self):
        if not self.deck:
            tk.messagebox.showwarning("No more cards", "The deck is empty!")
            return
        for _ in range(3):
            if self.deck:
                self.table.append(self.deck.pop())
        self.deck_label.config(text=f"Deck: {len(self.deck)}")
        self.draw_table()

if __name__ == "__main__":
    root = tk.Tk()
    game = SetCardGame(root)
    root.mainloop()
