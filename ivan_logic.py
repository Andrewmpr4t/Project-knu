# ── ivan_logic.py — Ігрова логіка (Іван) ─────────────────────────────────────
# Чисті функції без UI: рух шашок, бої, перевірка переможця.
# Значення клітинок: 0=пусто, 1=біла, 2=чорна, 3=біла дамка, 4=чорна дамка

DIRS = [(-1,-1),(-1,1),(1,-1),(1,1)]  # 4 діагональні напрямки

def owner(p):
    """Повертає номер гравця (1 або 2), або 0 якщо клітинка пуста."""
    return 1 if p in (1,3) else (2 if p in (2,4) else 0)

def is_king(p):
    """Чи є шашка дамкою."""
    return p in (3,4)

def get_jumps(board, r, c, turn):
    """
    Повертає словник можливих боїв для шашки на (r,c).
    Ключ — клітинка приземлення, значення — клітинка збитої шашки.
    Дамка б'є по всій діагоналі, звичайна — через одну клітинку.
    """
    p = board[r][c]
    jumps = {}
    for dr, dc in DIRS:
        if is_king(p):
            # Скануємо діагональ: шукаємо ворога, потім вільні клітинки за ним
            nr, nc, enemy = r+dr, c+dc, None
            while 0 <= nr < 8 and 0 <= nc < 8:
                cell = board[nr][nc]
                if enemy is None:
                    if owner(cell) == 3-turn: enemy = (nr,nc)  # знайшли ворога
                    elif cell: break                            # своя шашка — стоп
                else:
                    if cell == 0: jumps[(nr,nc)] = enemy       # посадка за ворогом
                    else: break                                 # шашка блокує
                nr += dr; nc += dc
        else:
            # Звичайна шашка: одна клітинка через ворога
            mr, mc = r+dr, c+dc
            er, ec = r+2*dr, c+2*dc
            if 0<=er<8 and 0<=ec<8 and owner(board[mr][mc])==3-turn and board[er][ec]==0:
                jumps[(er,ec)] = (mr,mc)
    return jumps

def get_moves(board, r, c):
    """
    Повертає словник тихих ходів (без бою).
    Білі (1) — вгору, чорні (2) — вниз, дамки — вся діагональ.
    """
    p = board[r][c]
    dirs = DIRS if is_king(p) else ([(-1,-1),(-1,1)] if p==1 else [(1,-1),(1,1)])
    moves = {}
    for dr, dc in dirs:
        nr, nc = r+dr, c+dc
        while 0<=nr<8 and 0<=nc<8 and board[nr][nc]==0:
            moves[(nr,nc)] = None
            if not is_king(p): break  # звичайна шашка — лише одна клітинка
            nr+=dr; nc+=dc
    return moves

def all_jumps(board, turn):
    """Збирає всі обов'язкові бої для поточного гравця по всій дошці."""
    result = {}
    for r in range(8):
        for c in range(8):
            if owner(board[r][c]) == turn:
                j = get_jumps(board, r, c, turn)
                if j: result[(r,c)] = j
    return result

def has_any_move(board, turn):
    """Перевіряє, чи є хоча б один тихий хід у поточного гравця."""
    for r in range(8):
        for c in range(8):
            if owner(board[r][c]) == turn and get_moves(board,r,c):
                return True
    return False