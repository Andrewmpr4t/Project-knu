import tkinter as tk
from tkinter import messagebox
SQ = 80

COLORS = {
    "light": "#f0d9b5", "dark":  "#b58863", "bg":   "#2b2b2b",
    "p1":    "#ffffff", "p2":    "#262626", "king": "#ffd700",
    "sel":   "#7fa650", "move":  "#99cc66",
}


class Menu(tk.Frame):
    def __init__(self, parent, on_play):
        super().__init__(parent, bg=COLORS["bg"])
        tk.Label(self, text="НАШІ ШАШКИ", font=("Helvetica",36,"bold"),
                 fg="white", bg=COLORS["bg"]).pack(pady=(120,50))
        def btn(text, color, cmd):
            tk.Button(self, text=text, font=("Helvetica",16,"bold"), width=25, height=2,
                      bg=color, fg="white", activebackground=color, cursor="hand2",
                      command=cmd).pack(pady=10)

        btn("Класичні шашки", "#4caf50", on_play)
        btn("Турецькі шашки", "#ff9800",
            lambda: messagebox.showinfo("В розробці", "Скоро буде!"))
        tk.Button(self, text="САМОЗНИЩЕННЯ", font=("Helvetica",14), width=20,
                  bg="#f44336", fg="white", cursor="hand2",
                  command=parent.quit).pack(pady=(40,0))

