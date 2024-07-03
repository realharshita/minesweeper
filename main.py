import tkinter as tk
import random
from tkinter import messagebox
import json
import os

class StartMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper - Start Menu")
        self.difficulty = "Medium"

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

        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game, font=("Helvetica", 14), bg="green", fg="white")
        self.start_button.pack(pady=20)

        self.help_button = tk.Button(self.master, text="Help", command=self.show_help, font=("Helvetica", 12), bg="blue", fg="white")
        self.help_button.pack(pady=5)

    def start_game(self):
        self.difficulty = self.difficulty_var.get()
        self.master.destroy()
        root = tk.Tk()
        MinesweeperGame(root, self.difficulty)
        root.mainloop()

    def show_help(self):
        help_window = tk.Toplevel(self.master)
        HelpMenu(help_window)

class HelpMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper - Help")

        instructions = (
            "Welcome to Minesweeper!\n\n"
            "The goal of the game is to reveal all the cells without mines.\n"
            "Left-click to reveal a cell.\n"
            "Right-click to flag/unflag a cell as a mine.\n\n"
            "Difficulty Levels:\n"
            "Easy: 8x8 grid with 10 mines\n"
            "Medium: 10x10 grid with 20 mines\n"
            "Hard: 12x12 grid with 30 mines\n\n"
            "Good luck!"
        )

        self.label = tk.Label(self.master, text=instructions, font=("Helvetica", 12), justify=tk.LEFT)
        self.label.pack(pady=10, padx=10)

        self.close_button = tk.Button(self.master, text="Close", command=self.master.destroy, font=("Helvetica", 12), bg="red", fg="white")
        self.close_button.pack(pady=10)

class MinesweeperGame:
    def __init__(self, master, difficulty):
        self.master = master
        self.master.title("Minesweeper")

        self.set_difficulty(difficulty)
        
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

    def set_difficulty(self, difficulty):
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

    def create_widgets(self):
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(pady=10)

        self.info_frame = tk.Frame(self.top_frame)
        self.info_frame.pack(side=tk.RIGHT)

        self.mine_counter = tk.Label(self.info_frame, text=f"Mines left: {self.mines - self.flags}", font=("Helvetica", 12))
        self.mine_counter.pack()

        self.timer_label = tk.Label(self.info_frame, text="Time: 0", font=("Helvetica", 12))
        self.timer_label.pack()

        self.score_label = tk.Label(self.info_frame, text=f"Score: {self.score}", font=("Helvetica", 12))
        self.score_label.pack()

        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()

        self.create_board_buttons()

        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack(pady=10)

        self.restart_button = tk.Button(self.control_frame, text="Restart", command=self.restart_game, font=("Helvetica", 12), bg="orange")
        self.restart_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.control_frame, text="Pause", command=self.pause_timer, font=("Helvetica", 12), bg="yellow")
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.resume_button = tk.Button(self.control_frame, text="Resume", command=self.resume_timer, font=("Helvetica", 12), bg="light green")
        self.resume_button.pack(side=tk.LEFT, padx=5)

    def create_board_buttons(self):
        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.board_frame, width=2, height=1, font=("Helvetica", 10, "bold"))
                button.bind('<Button-1>', lambda e, r=r, c=c: self.on_left_click(r, c))
                button.bind('<Button-3>', lambda e, r=r, c=c: self.on_right_click(r, c))
                button.grid(row=r, column=c)
                self.buttons[r][c] = button

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.board[r][c] != -1:
                self.board[r][c] = -1
                mines_placed += 1
    
    def calculate_adjacent_mines(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                mine_count = 0
                for dr, dc in directions:
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < self.rows and 0 <= cc < self.cols and self.board[rr][cc] == -1:
                        mine_count += 1
                self.board[r][c] = mine_count

    def on_left_click(self, r, c):
        if not self.timer_running:
            self.start_timer()
        
        if self.buttons[r][c]['text'] == 'F' or self.buttons[r][c]['state'] == 'disabled':
            return
        
        if self.board[r][c] == -1:
            self.buttons[r][c].config(text='*', bg='red')
            self.reveal_mines()
            self.stop_timer()
            messagebox.showinfo("Game Over", "You clicked on a mine!")
            self.update_leaderboard()
        else:
            self.reveal_cell(r, c)
            if self.check_win():
                self.stop_timer()
                messagebox.showinfo("Congratulations", "You win!")
                self.update_leaderboard()

    def on_right_click(self, r, c):
        if self.buttons[r][c]['text'] == 'F':
            self.buttons[r][c].config(text='', bg='SystemButtonFace')
            self.flags -= 1
            self.score -= 5
        else:
            self.buttons[r][c].config(text='F', bg='yellow')
            self.flags += 1
            self.score += 5
        self.mine_counter.config(text=f"Mines left: {self.mines - self.flags}")
        self.score_label.config(text=f"Score: {self.score}")

    def reveal_cell(self, r, c):
        if self.buttons[r][c]['state'] == 'disabled':
            return
        color_map = {1: 'blue', 2: 'green', 3: 'red', 4: 'purple', 5: 'maroon', 6: 'turquoise', 7: 'black', 8: 'gray'}
        if self.board[r][c] == 0:
            self.buttons[r][c].config(text='', bg='light gray', state='disabled', relief=tk.SUNKEN)
        else:
            self.buttons[r][c].config(text=str(self.board[r][c]), fg=color_map.get(self.board[r][c], 'black'), bg='light gray', state='disabled', relief=tk.SUNKEN)
            self.score += self.board[r][c] * 10
        self.revealed_cells += 1
        self.score_label.config(text=f"Score: {self.score}")
        if self.board[r][c] == 0:
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in directions:
                rr, cc = r + dr, c + dc
                if 0 <= rr < self.rows and 0 <= cc < self.cols:
                    self.reveal_cell(rr, cc)

    def reveal_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1 and self.buttons[r][c]['text'] != 'F':
                    self.buttons[r][c].config(text='*', bg='red')
                elif self.board[r][c] != -1 and self.buttons[r][c]['text'] == 'F':
                    self.buttons[r][c].config(text='X', bg='red')

    def check_win(self):
        return self.revealed_cells == self.rows * self.cols - self.mines

    def start_timer(self):
        self.timer_running = True
        self.time_elapsed = 0
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.time_elapsed += 1
            self.timer_label.config(text=f"Time: {self.time_elapsed}")
            self.master.after(1000, self.update_timer)

    def stop_timer(self):
        self.timer_running = False

    def pause_timer(self):
        self.timer_running = False

    def resume_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def restart_game(self):
        self.master.destroy()
        root = tk.Tk()
        StartMenu(root)
        root.mainloop()

    def update_leaderboard(self):
        try:
            with open("leaderboard.json", "r") as file:
                leaderboard = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            leaderboard = []

        leaderboard.append({"time": self.time_elapsed, "score": self.score})
        leaderboard = sorted(leaderboard, key=lambda x: (x["time"], -x["score"]))[:10]

        with open("leaderboard.json", "w") as file:
            json.dump(leaderboard, file, indent=4)

        self.show_leaderboard(leaderboard)

    def show_leaderboard(self, leaderboard):
        leaderboard_window = tk.Toplevel(self.master)
        leaderboard_window.title("Leaderboard")
        
        leaderboard_text = "Leaderboard:\n\n"
        for idx, entry in enumerate(leaderboard):
            leaderboard_text += f"{idx + 1}. Time: {entry['time']}s, Score: {entry['score']}\n"
        
        leaderboard_label = tk.Label(leaderboard_window, text=leaderboard_text, font=("Helvetica", 12), justify=tk.LEFT)
        leaderboard_label.pack(pady=10, padx=10)
        
        close_button = tk.Button(leaderboard_window, text="Close", command=leaderboard_window.destroy, font=("Helvetica", 12), bg="red", fg="white")
        close_button.pack(pady=10)

def main():
    root = tk.Tk()
    app = StartMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
