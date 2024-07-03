import tkinter as tk
import random
from tkinter import messagebox

class MinesweeperGame:
    def __init__(self, master):
        self.master = master
        self.rows = 10
        self.cols = 10
        self.mines = 20
        
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

    def create_widgets(self):
        self.difficulty_frame = tk.Frame(self.master)
        self.difficulty_frame.pack()

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("Medium")

        tk.Radiobutton(self.difficulty_frame, text="Easy", variable=self.difficulty_var, value="Easy", command=self.set_difficulty).pack(side=tk.LEFT)
        tk.Radiobutton(self.difficulty_frame, text="Medium", variable=self.difficulty_var, value="Medium", command=self.set_difficulty).pack(side=tk.LEFT)
        tk.Radiobutton(self.difficulty_frame, text="Hard", variable=self.difficulty_var, value="Hard", command=self.set_difficulty).pack(side=tk.LEFT)

        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()
        
        self.create_board_buttons()

        self.mine_counter = tk.Label(self.master, text=f"Mines left: {self.mines - self.flags}")
        self.mine_counter.pack()

        self.timer_label = tk.Label(self.master, text="Time: 0")
        self.timer_label.pack()

        self.score_label = tk.Label(self.master, text=f"Score: {self.score}")
        self.score_label.pack()

        self.restart_button = tk.Button(self.master, text="Restart", command=self.restart_game)
        self.restart_button.pack()

        self.pause_button = tk.Button(self.master, text="Pause", command=self.pause_timer)
        self.pause_button.pack()

        self.resume_button = tk.Button(self.master, text="Resume", command=self.resume_timer)
        self.resume_button.pack()

    def create_board_buttons(self):
        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.board_frame, width=2, height=1)
                button.bind('<Button-1>', lambda e, r=r, c=c: self.on_left_click(r, c))
                button.bind('<Button-3>', lambda e, r=r, c=c: self.on_right_click(r, c))
                button.grid(row=r, column=c)
                self.buttons[r][c] = button
        
    def set_difficulty(self):
        difficulty = self.difficulty_var.get()
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
        self.restart_game()

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
        else:
            self.reveal_cell(r, c)
            if self.check_win():
                self.stop_timer()
                messagebox.showinfo("Congratulations", "You win!")

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
        if self.board[r][c] == 0:
            self.buttons[r][c].config(text='', bg='light grey', state='disabled')
            for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                rr, cc = r + dr, c + dc
                if 0 <= rr < self.rows and 0 <= cc < self.cols:
                    self.reveal_cell(rr, cc)
        else:
            self.buttons[r][c].config(text=str(self.board[r][c]), bg='light grey', state='disabled')
        self.revealed_cells += 1
        self.score += 10
        self.score_label.config(text=f"Score: {self.score}")

    def reveal_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    self.buttons[r][c].config(text='*', bg='red')

    def check_win(self):
        return self.revealed_cells == self.rows * self.cols - self.mines

    def restart_game(self):
        self.board_frame.destroy()  
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()
        
        self.buttons = [[None] * self.cols for _ in range(self.rows)]
        self.create_board_buttons()

        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.revealed_cells = 0
        self.flags = 0
        self.time_elapsed = 0
        self.score = 0
        self.timer_label.config(text="Time: 0")
        self.score_label.config(text=f"Score: {self.score}")
        self.timer_running = False
        self.place_mines()
        self.calculate_adjacent_mines()
        self.mine_counter.config(text=f"Mines left: {self.mines}")

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def pause_timer(self):
        self.timer_running = False

    def resume_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.time_elapsed += 1
            self.timer_label.config(text=f"Time: {self.time_elapsed}")
            self.master.after(1000, self.update_timer)

def main():
    root = tk.Tk()
    root.title("Minesweeper")
    game = MinesweeperGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
