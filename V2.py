import tkinter as tk
from tkinter import messagebox
import time

# ---------- Sudoku configuration ----------
N = 6          # board size (N x N)
BR = 2         # block height
BC = 3         # block width
SYMBOLS = list(range(1, N + 1))
DELAY = 0.02   # delay for solving animation (seconds)

# Initial board (0 = empty). Keep or replace with your own puzzle.
Table = [[0] * N for _ in range(N)]


# ---------- Validation helpers ----------
def is_valid(board, row, col, num):
    """Return True if 'num' can be placed at board[row][col] under Sudoku rules."""
    # Row check
    if num in board[row]:
        return False

    # Column check
    for r in range(N):
        if board[r][col] == num:
            return False

    # BR x BC block check
    corner_row = row - (row % BR)
    corner_col = col - (col % BC)
    for x in range(BR):
        for y in range(BC):
            if board[corner_row + x][corner_col + y] == num:
                return False

    return True


def is_sudoku_valid(board):
    """Validate the entire current board (useful for user-entered puzzles)."""
    for r in range(N):
        for c in range(N):
            num = board[r][c]
            if num != 0:
                board[r][c] = 0  # temporarily clear to test placement
                ok = is_valid(board, r, c, num)
                board[r][c] = num
                if not ok:
                    return False
    return True


# ---------- Backtracking solver ----------
def solve(board, row, col, update_ui):
    """Solve Sudoku via backtracking; calls update_ui() to animate."""
    # Move to next row when we pass the last column
    if col == N:
        if row == N - 1:  # finished last cell
            return True
        row += 1
        col = 0

    # Skip pre-filled cells
    if board[row][col] > 0:
        return solve(board, row, col + 1, update_ui)

    # Try all candidates
    for num in SYMBOLS:
        if is_valid(board, row, col, num):
            board[row][col] = num
            update_ui()
            time.sleep(DELAY)
            if solve(board, row, col + 1, update_ui):
                return True

        # Backtrack
        board[row][col] = 0
        update_ui()
        time.sleep(DELAY)

    return False


# ---------- UI ----------
def create_ui():
    """Create and run the Tkinter UI."""
    def solve_sudoku():
        # Read user input from entries into Table
        for i in range(N):
            for j in range(N):
                val = entries[i][j].get().strip()
                if val.isdigit():
                    x = int(val)
                    Table[i][j] = x if (1 <= x <= N) else 0
                else:
                    Table[i][j] = 0

        # Validate puzzle before solving
        if not is_sudoku_valid(Table):
            messagebox.showerror("Invalid Sudoku", "The puzzle has conflicts (row/column/block).")
            return

        # Solve
        if solve(Table, 0, 0, update_ui):
            messagebox.showinfo("Solved", "Sudoku solved successfully!")
        else:
            messagebox.showinfo("No Solution", "No solution exists for this puzzle.")

    def update_ui():
        # Reflect Table -> entries and color cells
        for i in range(N):
            for j in range(N):
                text = "" if Table[i][j] == 0 else str(Table[i][j])
                if text != entries[i][j].get():
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, text)
                entries[i][j].configure(bg="#c0ffc0" if Table[i][j] != 0 else "#f0f0f0")
        root.update()

    def clear_board():
        # Clear entire grid
        for i in range(N):
            for j in range(N):
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, "")
                entries[i][j].configure(bg="#ffffff")
                Table[i][j] = 0

    def on_entry_change(event, i, j):
        # Live coloring for user input validity
        val = entries[i][j].get().strip()
        if val == "":
            entries[i][j].configure(bg="#ffffff")
        elif val.isdigit() and 1 <= int(val) <= N:
            entries[i][j].configure(bg="#c0ffc0")
        else:
            entries[i][j].configure(bg="#ffcccc")

    # Window
    root = tk.Tk()
    root.title(f"Sudoku {N}×{N} Solver (Blocks {BR}×{BC})")

    # Board frame
    frame = tk.Frame(root, bg="black")
    frame.pack(padx=10, pady=10)

    # Grid of entries
    global entries
    entries = []
    for i in range(N):
        row_entries = []
        for j in range(N):
            e = tk.Entry(
                frame,
                width=2,
                font=("Arial", 22),
                justify="center",
                borderwidth=2,
                relief="solid",
            )
            # Thick spacing between blocks
            padx = (0 if (j + 1) % BC else 5)
            pady = (0 if (i + 1) % BR else 5)
            e.grid(row=i, column=j, padx=padx, pady=pady)

            if Table[i][j] != 0:
                e.insert(0, str(Table[i][j]))
                e.configure(bg="#c0ffc0")
            else:
                e.configure(bg="#f0f0f0")

            e.bind("<KeyRelease>", lambda ev, x=i, y=j: on_entry_change(ev, x, y))
            row_entries.append(e)
        entries.append(row_entries)

    # Buttons
    tk.Button(
        root, text="Solve", font=("Arial", 14), command=solve_sudoku, bg="#4caf50", fg="white"
    ).pack(pady=8)

    tk.Button(
        root, text="Clear Board", font=("Arial", 14), command=clear_board, bg="#f44336", fg="white"
    ).pack(pady=4)

    root.mainloop()


# Run the app
create_ui()
