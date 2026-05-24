import tkinter as tk
from tkinter import messagebox
import pygame 
SQ = 80
COLORS = {
    "light": "#f0d9b5", "dark":  "#b58863", "bg":   "#2b2b2b",
    "p1":    "#ffffff", "p2":    "#262626", "king": "#ffd700",
    "sel":   "#7fa650", "move":  "#99cc66",
}

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        

        self.track_start = "start.mp3"  
        self.track_mid = "mid.mp3"    
        self.track_fin = "fin.mp3"    
      
        
        self.current_phase = 0  

    def play_phase(self, phase):
        if phase == self.current_phase:
            return  

        track = None
        if phase == 1 and self.track_start: track = self.track_start
        elif phase == 2 and self.track_mid: track = self.track_mid
        elif phase == 3 and self.track_fin: track = self.track_fin

        if track:
            try:
                pygame.mixer.music.load(track)
                pygame.mixer.music.play(-1)
                self.current_phase = phase
            except Exception as e:
                print(f"Помилка завантаження треку {track}: {e}")

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
            lambda: messagebox.showinfo("Турки схоже працюють?", "Зачекайте повернення!"))
        tk.Button(self, text="САМОЗНИЩЕННЯ", font=("Helvetica",14), width=20,
                  bg="#f44336", fg="white", cursor="hand2",
                  command=parent.quit).pack(pady=(40,0))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        from anton_game import Game

        self.title("Наші Шашки")
        self.geometry(f"{8*SQ}x{8*SQ+76}"); self.resizable(False, False)

        
        self.audio = AudioManager()

        self.menu = Menu(self, self.play)
        self.game = Game(self, self.show_menu)
        self.show_menu()

    def show_menu(self):
        pygame.mixer.music.stop() 
        self.audio.current_phase = 0
        self.game.pack_forget()
        self.menu.pack(fill=tk.BOTH, expand=True)

    def play(self):
        self.menu.pack_forget()
        self.game.reset()
        self.game.pack(fill=tk.BOTH, expand=True)
        self.audio.play_phase(1)


if __name__ == "__main__":
    App().mainloop()
    

