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


def reset(self):
        """Скидає дошку до початкового стану."""
        b = [[0]*8 for _ in range(8)]
        for r in range(3):    # чорні шашки — рядки 0-2
            for c in range(8):
                if (r+c)%2: b[r][c] = 2
        for r in range(5,8):  # білі шашки — рядки 5-7
            for c in range(8):
                if (r+c)%2: b[r][c] = 1
        self.board = b
        self.turn   = 1     # білі ходять першими
        self.sel    = None  # виділена шашка (r,c)
        self.moves  = {}    # доступні ходи для виділеної шашки
        self.forced = None  # шашка, що продовжує серію боїв
        self.jumps  = all_jumps(b, 1)
        self.draw()

def click(self, e):
        """Обробляє клік по дошці."""
        c, r = e.x//SQ, e.y//SQ
        if not (0<=r<8 and 0<=c<8): return

        # Якщо шашка виділена — намагаємось зробити хід
        if self.sel:
            if (r,c) in self.moves:
                self.do_move(self.sel[0], self.sel[1], r, c); return
            # Клік по тій самій шашці — знімаємо виділення (якщо не в серії боїв)
            if (r,c) == self.sel and not self.forced:
                self.sel = None; self.moves = {}; self.draw(); return
        # Вибираємо шашку поточного гравця
        if owner(self.board[r][c]) == self.turn:
            if self.forced and self.forced != (r,c): return  # тільки продовження серії
            if self.jumps:
                if (r,c) not in self.jumps: return           # обов'язковий бій
                self.moves = self.jumps[(r,c)]
            else:
                self.moves = get_moves(self.board, r, c)
            self.sel = (r,c); self.draw()

    def do_move(self, sr, sc, er, ec):
        """Виконує хід із (sr,sc) в (er,ec)."""
        jumped = self.moves[(er,ec)]  # позиція збитої шашки або None
        p = self.board[sr][sc]
        self.board[er][ec] = p; self.board[sr][sc] = 0

# Перетворення на дамку при досягненні останнього рядка
        made_king = False
        if p==1 and er==0: self.board[er][ec]=3; made_king=True
        elif p==2 and er==7: self.board[er][ec]=4; made_king=True

        if jumped:
            self.board[jumped[0]][jumped[1]] = 0  # прибираємо збиту шашку
            # Якщо не стали дамкою — перевіряємо продовження серії боїв
            if not made_king:
                nj = get_jumps(self.board, er, ec, self.turn)
                if nj:
                    self.sel=(er,ec); self.moves=nj
                    self.forced=(er,ec); self.jumps={(er,ec):nj}
                    self.draw(); return

        # Завершуємо хід, передаємо чергу
        self.sel=None; self.moves={}; self.forced=None
        self.turn = 3-self.turn
        self.jumps = all_jumps(self.board, self.turn)
        self.draw()

        # Перевіряємо переможця: суперник не може ходити — програв
        if not self.jumps and not has_any_move(self.board, self.turn):
            winner = "Білі" if self.turn==2 else "Чорні"
            messagebox.showinfo("ГГ", f"{winner} перемогли!")
            self.reset()
    def draw(self):
        """Перемальовує всю дошку та індикатор ходу."""
        cv = self.canvas; cv.delete("all")

# Оновлюємо кружок і текст індикатора ходу
        self.dot.delete("all")
        self.dot.create_oval(2,2,18,18, fill=COLORS["p1" if self.turn==1 else "p2"],
                             outline="#888", width=1)
        self.lbl.config(text="Хід: Білі" if self.turn==1 else "Хід: Чорні")

        for r in range(8):
            for c in range(8):
                # Колір клітинки: базовий / виділена / доступний хід
