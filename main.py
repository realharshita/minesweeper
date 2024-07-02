import random
BOARD_SIZE = 8
NUM_MINES = 10

def initialize_board(size, num_mines):
    board = [[' ' for _ in range(size)] for _ in range(size)]
    
    mines_placed = 0
    while mines_placed < num_mines:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        if board[row][col] != 'X':
            board[row][col] = 'X'
            mines_placed += 1
            
    return board

def display_board(board, show_mines=False):
    size = len(board)
    for row in range(size):
        for col in range(size):
            if not show_mines and board[row][col] == 'X':
                print(' ', end=' ')
            else:
                print(board[row][col], end=' ')
        print()

def uncover_cell(board, row, col):
    if board[row][col] == 'X':
        return False
    else:
        uncover_recursive(board, row, col)
        return True

def uncover_recursive(board, row, col):
    size = len(board)
    if board[row][col] == ' ':
        board[row][col] = '0'
        for i in range(max(0, row-1), min(size, row+2)):
            for j in range(max(0, col-1), min(size, col+2)):
                if board[i][j] == ' ':
                    uncover_recursive(board, i, j)
                elif board[i][j] == 'X':
                    board[i][j] = '1' if board[i][j] == ' ' else ' '

def main():
    board = initialize_board(BOARD_SIZE, NUM_MINES)
    game_over = False
    
    while not game_over:
        print("Current Board:")
        display_board(board)
        
        try:
            row = int(input("Enter row (0-7): "))
            col = int(input("Enter column (0-7): "))
            
            if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
                print("Invalid input. Please enter numbers between 0 and 7.")
                continue
            
            if not uncover_cell(board, row, col):
                print("Game Over! You uncovered a mine.")
                print("Final Board:")
                display_board(board, show_mines=True)
                game_over = True
            else:
                print("Cell uncovered successfully.")
                
                uncovered_count = sum(row.count(' ') for row in board)
                if uncovered_count == NUM_MINES:
                    print("Congratulations! You win!")
                    game_over = True
        
        except ValueError:
            print("Invalid input. Please enter integers.")
        except KeyboardInterrupt:
            print("\nGame aborted. Exiting...")
            break

if __name__ == "__main__":
    main()
