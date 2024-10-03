import tkinter as tk
from tkinter import messagebox
import time

# Initial Sudoku table (0 represents empty cells)
Table = [
    [3, 0, 6, 5, 0, 8, 4, 0, 0],
    [5, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 7, 0, 0, 0, 0, 3, 1],
    [0, 0, 3, 0, 1, 0, 0, 8, 0],
    [9, 0, 0, 8, 6, 3, 0, 0, 5],
    [0, 5, 0, 0, 9, 0, 6, 0, 0],
    [1, 3, 0, 0, 0, 0, 2, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 7, 4],
    [0, 0, 5, 2, 0, 6, 3, 0, 0],
]

# Function to check if placing a number in a specific row and column is valid
def is_valid(Table, row, col, num):
    # Check if number exists in the current row
    if num in Table[row]:
        return False

    # Check if number exists in the current column
    for x in range(9):
        if Table[x][col] == num:
            return False

    # Check if number exists in the 3x3 sub-grid
    corner_row = row - (row % 3)
    corner_col = col - (col % 3)

    for x in range(3):
        for y in range(3):
            if Table[corner_row + x][corner_col + y] == num:
                return False
    return True

# Function to check if the entire Sudoku board is valid
def is_sudoku_valid():
    for row in range(9):
        for col in range(9):
            num = Table[row][col]
            if num != 0:
                # Temporarily remove the number to check its validity
                Table[row][col] = 0
                if not is_valid(Table, row, col, num):
                    # If invalid, restore the number and return False
                    Table[row][col] = num
                    return False
                # Restore the number
                Table[row][col] = num
    return True

# Backtracking function to solve the Sudoku
def solve(Table, row, col, update_ui):
    # If we reach the end of the board
    if col == 9:
        if row == 8:
            return True
        else:
            row += 1
            col = 0

    # If the cell is already filled, move to the next cell
    if Table[row][col] > 0:
        return solve(Table, row, col + 1, update_ui)

    # Try placing numbers from 1 to 9 in the current cell
    for num in range(1, 10):
        if is_valid(Table, row, col, num):
            Table[row][col] = num
            update_ui()
            time.sleep(0.02)  # Small delay to visualize the solving process

            if solve(Table, row, col + 1, update_ui):
                return True

        # Backtrack if placing the number didn't lead to a solution
        Table[row][col] = 0
        update_ui()
        time.sleep(0.02)

    return False

# Function to create the GUI for Sudoku solver
def create_ui():
    # Function to handle solving the Sudoku after validating the user's input
    def solve_sudoku():
        # Save user's input in the Table array
        for i in range(9):
            for j in range(9):
                val = entries[i][j].get()
                if val.isdigit():
                    Table[i][j] = int(val)
                else:
                    Table[i][j] = 0

        # Validate the user's Sudoku before solving
        if not is_sudoku_valid():
            messagebox.showerror("Invalid Sudoku", "The entered Sudoku is not valid.")
            return

        # Solve the Sudoku if it's valid
        if solve(Table, 0, 0, update_ui):
            messagebox.showinfo("Solved", "Sudoku Solved Successfully!")
        else:
            messagebox.showinfo("No Solution", "No Solution For This Sudoku")

    # Function to update the UI after each step in the solving process
    def update_ui():
        for i in range(9):
            for j in range(9):
                if str(Table[i][j]) != entries[i][j].get():
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, str(Table[i][j]))
                    # Color the cell based on whether it's filled or empty
                    entries[i][j].configure(bg='#c0ffc0' if Table[i][j] != 0 else '#f0f0f0')
        root.update()

    # Function to clear the board and reset it for user input
    def clear_board():
        # Clear all cells and set background to white
        for i in range(9):
            for j in range(9):
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, "")
                entries[i][j].configure(bg='#ffffff')  # Set background to white
                Table[i][j] = 0

    # Function to handle changes in the cells (color them based on input validity)
    def on_entry_change(event, i, j):
        # Get the value entered by the user
        val = entries[i][j].get()
        if val.isdigit() and 1 <= int(val) <= 9:
            entries[i][j].configure(bg='#c0ffc0')  # Set background to green for valid input
        elif val == "":
            entries[i][j].configure(bg='#ffffff')  # Set background to white for empty cells
        else:
            entries[i][j].configure(bg='#ffcccc')  # Set background to red for invalid input

    # Initialize the main window
    root = tk.Tk()
    root.title("Solving Sudoku with Backtracking Algorithm")

    # Create a frame to hold the Sudoku grid
    frame = tk.Frame(root, bg="black")
    frame.pack(padx=10, pady=10)

    # Create a 9x9 grid of entry boxes for the Sudoku cells
    entries = []
    for i in range(9):
        row_entries = []
        for j in range(9):
            entry = tk.Entry(frame, width=2, font=('Arial', 18),
                             justify='center', borderwidth=2, relief='solid')
            entry.grid(row=i, column=j, padx=(0 if (j+1) % 3 else 5), pady=(0 if (i+1) % 3 else 5))
            entry.insert(0, str(Table[i][j]) if Table[i][j] != 0 else "")
            entry.configure(bg='#f0f0f0' if Table[i][j] == 0 else '#c0ffc0')
            entry.bind('<KeyRelease>', lambda event, x=i, y=j: on_entry_change(event, x, y))
            row_entries.append(entry)
        entries.append(row_entries)

    # Add the "Solve" button to start the solving process
    solve_button = tk.Button(root, text="Solve", font=('Arial', 14),
                             command=solve_sudoku, bg="#4caf50", fg="white")
    solve_button.pack(pady=10)

    # Add the "Clear Board" button to reset the grid for user input
    clear_button = tk.Button(root, text="Clear Board", font=('Arial', 14),
                             command=clear_board, bg="#f44336", fg="white")
    clear_button.pack(pady=10)

    # Start the main loop of the GUI
    root.mainloop()


# Run the Sudoku solver UI
create_ui()
