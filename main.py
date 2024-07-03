import tkinter as tk
import random
import json
from tkinter import messagebox

class StartMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper - Start Menu")
        self.difficulty = "Medium"
        self.theme = "Light"
        
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="Minesweeper", font=("Helvetica", 20, "bold"), fg="blue")
        self.title_label.pack(pady=10)

        self.difficulty_frame = tk.Frame(self.master)
        self.difficulty_frame.pack(pady=10)

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("Medium")

        tk.Radiobutton(self.difficulty_frame, text="Easy", variable=self.difficulty_var, value="Easy", font=("Helvetica", 12)).pack(side=tk.LEFT)
        tk.Radiobutton(self.difficulty_frame, text="Medium", variable=self.difficulty_var, value="Medium", font=("Helvetica", 12)).pack(side=tk.LEFT)
        tk.Radiobutton(self.difficulty_frame, text="Hard", variable=self.difficulty_var, value="Hard", font=("Helvetica", 12)).pack(side=tk.LEFT)
        tk.Radiobutton(self.difficulty_frame, text="Custom", variable=self.difficulty_var, value="Custom", font=("Helvetica", 12)).pack(side=tk.LEFT)

        self.theme_frame = tk.Frame(self.master)
        self.theme_frame.pack(pady=10)

        self.theme_var = tk.StringVar()
        self.theme_var.set("Light")

        tk.Radiobutton(self.theme_frame, text="Light Theme", variable=self.theme_var, value="Light", font=("Helvetica", 12)).pack(side=tk.LEFT)
        tk.Radiobutton(self.theme_frame, text="Dark Theme", variable=self.theme_var, value="Dark", font=("Helvetica", 12)).pack(side=tk.LEFT)

        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game, font=("Helvetica", 14), bg="green", fg="white")
        self.start_button.pack(pady=20)

        self.help_button = tk.Button(self.master, text="Help", command=self.show_help, font=("Helvetica", 14), bg="blue", fg="white")
        self.help_button.pack(pady=10)

    def start_game(self):
        self.difficulty = self.difficulty_var.get()
        self.theme = self.theme_var.get()
        if self.difficulty == "Custom":
            self.show_custom_difficulty_window()
        else:
            self.master.destroy()
            root = tk.Tk()
            MinesweeperGame(root, self.difficulty, self.theme)
            root.mainloop()

    def show_help(self):
        HelpMenu(self.master)

    def show_custom_difficulty_window(self):
        self.custom_window = tk.Toplevel(self.master)
        self.custom_window.title("Custom Difficulty")

        tk.Label(self.custom_window, text="Rows:", font=("Helvetica", 12)).pack(pady=5)
        self.rows_entry = tk.Entry(self.custom_window, font=("Helvetica", 12))
        self.rows_entry.pack(pady=5)

        tk.Label(self.custom_window, text="Columns:", font=("Helvetica", 12)).pack(pady=5)
        self.cols_entry = tk.Entry(self.custom_window, font=("Helvetica", 12))
        self.cols_entry.pack(pady=5)

        tk.Label(self.custom_window, text="Mines:", font=("Helvetica", 12)).pack(pady=5)
        self.mines_entry = tk.Entry(self.custom_window, font=("Helvetica", 12))
        self.mines_entry.pack(pady=5)

        self.custom_start_button = tk.Button(self.custom_window, text="Start", command=self.start_custom_game, font=("Helvetica", 12), bg="green", fg="white")
        self.custom_start_button.pack(pady=10)

    def start_custom_game(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            mines = int(self.mines_entry.get())
            if rows > 0 and cols > 0 and mines > 0:
                self.custom_window.destroy()
                self.master.destroy()
                root = tk.Tk()
                MinesweeperGame(root, self.difficulty, self.theme, custom_rows=rows, custom_cols=cols, custom_mines=mines)
                root.mainloop()
            else:
                messagebox.showerror("Invalid Input", "Rows, Columns, and Mines must be positive integers.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers for Rows, Columns, and Mines.")

class HelpMenu:
    def __init__(self, master):
        self.help_window = tk.Toplevel(master)
        self.help_window.title("Help")

        help_text = """
        Welcome to Minesweeper!

        Objective:
        - Uncover all the cells that do not contain mines.

        How to Play:
        - Left-click to reveal a cell.
        - Right-click to flag/unflag a cell as a mine.
        - Reveal all non-mine cells to win.

        Buttons:
        - Start Game: Begin a new game with selected difficulty and theme.
        - Restart: Restart the current game.
        - Pause: Pause the timer.
        - Resume: Resume the timer.
        - Help: Show this help menu.

        Good luck!
        """
        self.help_label = tk.Label(self.help_window, text=help_text, font=("Helvetica", 12), justify=tk.LEFT)
        self.help_label.pack(pady=10, padx=10)

        self.close_button = tk.Button(self.help_window, text="Close", command=self.help_window.destroy, font=("Helvetica", 12), bg="red", fg="white")
        self.close_button.pack(pady=10)

class MinesweeperGame:
    def __init__(self, master, difficulty, theme, custom_rows=None, custom_cols=None, custom_mines=None):
        self.master = master
        self.master.title("Minesweeper")

        self.theme = theme
        self.set_theme()
        
        self.set_difficulty(difficulty, custom_rows, custom_cols, custom_mines)
        
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.buttons = [[None] * self.cols for _ in range(self.rows)]
        self.flags = 0
        self.revealed_cells = 0
        self.timer_running = False
        self.time_elapsed = 0
        self.score = 0

        self.create_widgets()
        self.place_mines()
        self.calculate_adjacent_mines()

    def set_theme(self):
        if self.theme == "Light":
            self.bg_color = "SystemButtonFace"
            self.fg_color = "black"
            self.button_color = "light gray"
        elif self.theme == "Dark":
            self.bg_color = "black"
            self.fg_color = "white"
            self.button_color = "gray"
        self.master.configure(bg=self.bg_color)

    def set_difficulty(self, difficulty, custom_rows, custom_cols, custom_mines):
        if difficulty == "Easy":
            self.rows = 8
            self.cols = 8
            self.mines = 10
        elif difficulty == "Medium":
            self.rows = 10
            self.cols = 10
            self.mines = 20
        elif difficulty == "Hard":
            self.rows = 12
            self.cols = 12
            self.mines = 30
        elif difficulty == "Custom":
            self.rows = custom_rows
            self.cols = custom_cols
            self.mines = custom_mines

    def create_widgets(self):
        self.top_frame = tk.Frame(self.master, bg=self.bg_color)
        self.top_frame.pack(pady=10)

        self.info_frame = tk.Frame(self.top_frame, bg=self.bg_color)
        self.info_frame.pack(side=tk.RIGHT)

        self.mine_counter = tk.Label(self.info_frame, text=f"Mines left: {self.mines - self.flags}", font=("Helvetica", 12), bg=self.bg_color, fg=self.fg_color)
        self.mine_counter.pack()

        self.timer_label = tk.Label(self.info_frame, text="Time: 0", font=("Helvetica", 12), bg=self.bg_color, fg=self.fg_color)
        self.timer_label.pack()

        self.score_label = tk.Label(self.info_frame, text=f"Score: {self.score}", font=("Helvetica", 12), bg=self.bg_color, fg=self.fg_color)
        self.score_label.pack()

        self.board_frame = tk.Frame(self.master, bg=self.bg_color)
        self.board_frame.pack()

        self.create_board_buttons()

        self.control_frame = tk.Frame(self.master, bg=self.bg_color)
        self.control_frame.pack(pady=10)

        self.restart_button = tk.Button(self.control_frame, text="Restart", command=self.restart_game, font=("Helvetica", 12), bg="orange")
        self.restart_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.control_frame, text="Pause", command=self.pause, font=("Helvetica", 12), bg="yellow")
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.resume_button = tk.Button(self.control_frame, text="Resume", command=self.resume, font=("Helvetica", 12), bg="green")
        self.resume_button.pack(side=tk.LEFT, padx=5)

        self.return_button = tk.Button(self.control_frame, text="Return to Menu", command=self.return_to_menu, font=("Helvetica", 12), bg="red")
        self.return_button.pack(side=tk.LEFT, padx=5)

    def create_board_buttons(self):
        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.board_frame, text="", width=3, height=1, bg=self.button_color, command=lambda r=r, c=c: self.reveal_cell(r, c))
                button.bind("<Button-3>", lambda event, r=r, c=c: self.toggle_flag(r, c))
                button.grid(row=r, column=c)
                self.buttons[r][c] = button

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.board[r][c] == 0:
                self.board[r][c] = -1
                mines_placed += 1

    def calculate_adjacent_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                adjacent_mines = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if 0 <= r + dr < self.rows and 0 <= c + dc < self.cols and self.board[r + dr][c + dc] == -1:
                            adjacent_mines += 1
                self.board[r][c] = adjacent_mines

    def reveal_cell(self, r, c):
        if not self.timer_running:
            self.start_timer()

        if self.buttons[r][c]["state"] == tk.DISABLED:
            return

        if self.board[r][c] == -1:
            self.game_over(False)
            return

        self.reveal_button(r, c)

        if self.board[r][c] == 0:
            self.reveal_adjacent_cells(r, c)

        if self.revealed_cells == self.rows * self.cols - self.mines:
            self.game_over(True)

    def reveal_button(self, r, c):
        self.buttons[r][c].config(state=tk.DISABLED, relief=tk.SUNKEN)
        self.buttons[r][c].config(bg=self.button_color)
        self.revealed_cells += 1
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")

        if self.board[r][c] > 0:
            self.buttons[r][c].config(text=str(self.board[r][c]))

    def reveal_adjacent_cells(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.buttons[nr][nc]["state"] != tk.DISABLED:
                    self.reveal_cell(nr, nc)

    def toggle_flag(self, r, c):
        if self.buttons[r][c]["state"] == tk.DISABLED:
            return
        if self.buttons[r][c].cget("text") == "":
            self.buttons[r][c].config(text="F", bg="red")
            self.flags += 1
        else:
            self.buttons[r][c].config(text="", bg=self.button_color)
            self.flags -= 1
        self.mine_counter.config(text=f"Mines left: {self.mines - self.flags}")

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.time_elapsed += 1
            self.timer_label.config(text=f"Time: {self.time_elapsed}")
            self.master.after(1000, self.update_timer)

    def pause(self):
        self.timer_running = False

    def resume(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def game_over(self, win):
        self.timer_running = False
        result = "You Win!" if win else "Game Over!"
        stats = f"Time taken: {self.time_elapsed} seconds\nCells revealed: {self.revealed_cells}\nScore: {self.score}"
        messagebox.showinfo(result, stats)
        self.master.destroy()
        root = tk.Tk()
        StartMenu(root)
        root.mainloop()

    def restart_game(self):
        self.master.destroy()
        root = tk.Tk()
        MinesweeperGame(root, self.difficulty, self.theme, self.rows, self.cols, self.mines)
        root.mainloop()

    def return_to_menu(self):
        self.master.destroy()
        root = tk.Tk()
        StartMenu(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = StartMenu(root)
    root.mainloop()
