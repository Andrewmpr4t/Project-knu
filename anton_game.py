import tkinter as tk
from tkinter import messagebox
from andriy_main import SQ, COLORS
class Game(tk.Frame):
    """Екран гри: дошка, логіка кліків, малювання."""
    def __init__(self, parent, on_menu):
        super().__init__(parent)

        # Верхня панель із кнопкою повернення в меню
        bar = tk.Frame(self, bg=COLORS["bg"]); bar.pack(fill=tk.X)
        tk.Button(bar, text="← В меню", font=("Helvetica",12,"bold"),
                  bg="#607d8b", fg="white", cursor="hand2",
                  command=on_menu).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(bar, text="Класичні шашки", font=("Helvetica",12),
                 fg="white", bg=COLORS["bg"]).pack(side=tk.RIGHT, padx=10, pady=5)

        # Ігрове поле (Canvas)
        self.canvas = tk.Canvas(self, width=8*SQ, height=8*SQ, highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)

        # Нижня панель — індикатор чийого ходу (кружок + текст)
        bot = tk.Frame(self, bg=COLORS["bg"]); bot.pack(fill=tk.X)
        self.dot = tk.Canvas(bot, width=20, height=20, bg=COLORS["bg"], highlightthickness=0)
        self.dot.pack(side=tk.LEFT, padx=(14,6), pady=8)
        self.lbl = tk.Label(bot, text="", font=("Helvetica",13,"bold"),
                            fg="white", bg=COLORS["bg"])
        self.lbl.pack(side=tk.LEFT)
        self.reset()
