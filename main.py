import tkinter as tk
import random

class StartMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper Start Menu")
        
        self.difficulty = tk.StringVar(value="Easy")
        
        tk.Label(master, text="Select Difficulty:").pack(pady=10)
        
        tk.Radiobutton(master, text="Easy", variable=self.difficulty, value="Easy").pack(anchor=tk.W)
        tk.Radiobutton(master, text="Medium", variable=self.difficulty, value="Medium").pack(anchor=tk.W)
        tk.Radiobutton(master, text="Hard", variable=self.difficulty, value="Hard").pack(anchor=tk.W)
        
        tk.Button(master, text="Start Game", command=self.start_game).pack(pady=20)

    def start_game(self):
        self.master.destroy()
        root = tk.Tk()
        MinesweeperGame(root, self.difficulty.get())
        root.mainloop()

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
        self.start_timer()

        self.master.rowconfigure(1, weight=1)
        self.master.columnconfigure(0, weight=1)

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
        self.top_frame.grid(row=0, column=0, sticky="ew")

        self.timer_label = tk.Label(self.top_frame, text="Time: 0")
        self.timer_label.pack(side=tk.LEFT, padx=10)

        self.mine_counter = tk.Label(self.top_frame, text=f"Mines left: {self.mines}")
        self.mine_counter.pack(side=tk.LEFT, padx=10)

        self.score_label = tk.Label(self.top_frame, text="Score: 0")
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.restart_button = tk.Button(self.top_frame, text="Restart", command=self.restart_game)
        self.restart_button.pack(side=tk.RIGHT, padx=10)

        self.board_frame = tk.Frame(self.master)
        self.board_frame.grid(row=1, column=0, sticky="nsew")

        for r in range(self.rows):
            self.board_frame.rowconfigure(r, weight=1)
            for c in range(self.cols):
                self.board_frame.columnconfigure(c, weight=1)
                button = tk.Button(self.board_frame, text="", width=3, height=1,
                                   command=lambda r=r, c=c: self.reveal_cell(r, c))
                button.bind("<Button-3>", lambda event, r=r, c=c: self.flag_cell(r, c))
                button.grid(row=r, column=c, sticky="nsew")
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
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                mine_count = 0
                for i in range(max(0, r-1), min(self.rows, r+2)):
                    for j in range(max(0, c-1), min(self.cols, c+2)):
                        if self.board[i][j] == -1:
                            mine_count += 1
                self.board[r][c] = mine_count

    def reveal_cell(self, r, c):
        if self.buttons[r][c]["state"] == "disabled":
            return

        if not self.timer_running:
            self.start_timer()

        self.buttons[r][c]["state"] = "disabled"
        self.revealed_cells += 1

        if self.board[r][c] == -1:
            self.buttons[r][c]["text"] = "M"
            self.buttons[r][c]["bg"] = "red"
            self.game_over(False)
        else:
            self.buttons[r][c]["text"] = str(self.board[r][c])
            self.buttons[r][c]["bg"] = "lightgrey"
            self.buttons[r][c]["disabledforeground"] = self.get_text_color(self.board[r][c])
            self.score += 1
            self.update_score()

            if self.board[r][c] == 0:
                for i in range(max(0, r-1), min(self.rows, r+2)):
                    for j in range(max(0, c-1), min(self.cols, c+2)):
                        if self.buttons[i][j]["state"] != "disabled":
                            self.reveal_cell(i, j)

        if self.revealed_cells == self.rows * self.cols - self.mines:
            self.game_over(True)

    def flag_cell(self, r, c):
        if self.buttons[r][c]["state"] == "disabled":
            return

        if self.buttons[r][c]["text"] == "F":
            self.buttons[r][c]["text"] = ""
            self.flags -= 1
        else:
            self.buttons[r][c]["text"] = "F"
            self.flags += 1

        self.update_mine_counter()

    def game_over(self, won):
        self.stop_timer()
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    self.buttons[r][c]["text"] = "M"
                self.buttons[r][c]["state"] = "disabled"

        if won:
            self.show_message("Congratulations! You've won!")
        else:
            self.show_message("Game Over! You've lost!")

    def show_message(self, message):
        popup = tk.Toplevel()
        popup.title("Game Over")
        tk.Label(popup, text=message).pack(pady=10)
        tk.Button(popup, text="OK", command=popup.destroy).pack(pady=5)

    def restart_game(self):
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.buttons = [[None] * self.cols for _ in range(self.rows)]
        self.flags = 0
        self.revealed_cells = 0
        self.timer_running = False
        self.time_elapsed = 0
        self.score = 0
        self.time_elapsed = 0

        self.board_frame.destroy()
        self.top_frame.destroy()
        self.create_widgets()
        self.place_mines()
        self.calculate_adjacent_mines()

        self.timer_label.config(text="Time: 0")
        self.mine_counter.config(text=f"Mines left: {self.mines}")
        self.score_label.config(text=f"Score: {self.score}")

    def update_mine_counter(self):
        self.mine_counter.config(text=f"Mines left: {self.mines - self.flags}")

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.time_elapsed += 1
            self.timer_label.config(text=f"Time: {self.time_elapsed}")
            self.master.after(1000, self.update_timer)

    def stop_timer(self):
        self.timer_running = False

    def get_text_color(self, count):
        colors = {
            0: "black",
            1: "blue",
            2: "green",
            3: "red",
            4: "darkblue",
            5: "darkred",
            6: "cyan",
            7: "black",
            8: "grey"
        }
        return colors.get(count, "black")

if __name__ == "__main__":
    root = tk.Tk()
    app = StartMenu(root)
    root.mainloop()
