import tkinter as tk
from tkinter import messagebox, simpledialog
import math
import copy

class GrandTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Grand Tic Tac Toe")
        self.main_board = [[' '] * 9 for _ in range(9)]
        self.sub_winners = [' '] * 9
        self.buttons = [[None] * 9 for _ in range(9)]
        self.frames = [None] * 9

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=5)

        self.restart_button = tk.Button(self.top_frame, text="Restart Game", command=self.restart_game, font=('Arial', 12))
        self.restart_button.pack(side="left", padx=10)

        self.cursor_label = tk.Label(self.top_frame, text="", font=('Arial', 16))
        self.cursor_label.pack(side="left", padx=10)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        for bi in range(9):
            sub_frame = tk.Frame(self.board_frame, borderwidth=3, relief="solid")
            sub_frame.grid(row=bi//3, column=bi%3, padx=4, pady=4)
            self.frames[bi] = sub_frame
            for i in range(9):
                btn = tk.Button(sub_frame, text=' ', font=('Arial', 14), height=2, width=4,
                                command=lambda bi=bi, i=i: self.player_move(bi, i))
                btn.grid(row=i//3, column=i%3, padx=1, pady=1)
                self.buttons[bi][i] = btn

        self.human_player = simpledialog.askstring("Player Choice", "Do you want to be X or O?").upper()
        self.ai_player = 'O' if self.human_player == 'X' else 'X'
        self.current_player = 'X'
        self.active_board = -1
        self.max_depth = 3

        self.update_cursor()
        if self.current_player == self.ai_player:
            self.root.after(500, self.ai_move)

    def restart_game(self):
        for bi in range(9):
            self.sub_winners[bi] = ' '
            for i in range(9):
                self.main_board[bi][i] = ' '
                self.buttons[bi][i].config(text=' ', bg='SystemButtonFace', state='normal')
        self.active_board = -1
        self.current_player = 'X'
        self.update_cursor()
        self.update_button_states()

        if self.current_player == self.ai_player:
            self.root.after(500, self.ai_move)

    def is_board_full(self, board_index):
        return all(cell != ' ' for cell in self.main_board[board_index])

    def check_winner(self, board):
        combos = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for combo in combos:
            if board[combo[0]] != ' ' and all(board[i] == board[combo[0]] for i in combo):
                return board[combo[0]]
        return ' '

    def is_draw(self, board):
        return ' ' not in board

    def player_move(self, board_index, cell_index):
        if self.current_player != self.human_player:
            return

        if (self.active_board == -1 and self.main_board[board_index][cell_index] == ' ') or \
           (self.active_board != -1 and (
               (board_index == self.active_board and self.main_board[board_index][cell_index] == ' ') or
               (self.is_board_full(self.active_board) and self.main_board[board_index][cell_index] == ' ')
           )):

            self.main_board[board_index][cell_index] = self.current_player
            self.buttons[board_index][cell_index].config(text=self.current_player, state='disabled')

            winner = self.check_winner(self.main_board[board_index])
            if winner != ' ':
                self.sub_winners[board_index] = winner
                for b in self.buttons[board_index]:
                    b.config(bg='lightgreen' if winner == 'X' else 'lightblue')

                self.buttons[board_index][cell_index].config(bg='yellow')

            if self.check_winner(self.sub_winners) != ' ':
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins the game!")
                self.root.quit()
                return
            elif all(w != ' ' for w in self.sub_winners):
                messagebox.showinfo("Game Over", "It's a draw!")
                self.root.quit()
                return

            if not self.is_board_full(cell_index):
                self.active_board = cell_index
            else:
                self.active_board = -1

            self.current_player = self.ai_player
            self.update_button_states()
            self.update_cursor()
            self.root.after(500, self.ai_move)

    def ai_move(self):
        board_index, cell_index = self.find_best_move()
        self.main_board[board_index][cell_index] = self.ai_player
        self.buttons[board_index][cell_index].config(text=self.ai_player, state='disabled')

        winner = self.check_winner(self.main_board[board_index])
        if winner != ' ':
            self.sub_winners[board_index] = winner
            for b in self.buttons[board_index]:
                b.config(bg='lightgreen' if winner == 'X' else 'lightblue')

            self.buttons[board_index][cell_index].config(bg='yellow')

        if self.check_winner(self.sub_winners) != ' ':
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins the game!")
            self.root.quit()
            return
        elif all(w != ' ' for w in self.sub_winners):
            messagebox.showinfo("Game Over", "It's a draw!")
            self.root.quit()
            return

        if not self.is_board_full(cell_index):
            self.active_board = cell_index
        else:
            self.active_board = -1

        self.current_player = self.human_player
        self.update_button_states()
        self.update_cursor()

    def evaluate(self, sub_winners):
        winner = self.check_winner(sub_winners)
        if winner == self.ai_player:
            return 10
        elif winner == self.human_player:
            return -10
        return 0

    def find_best_move(self):
        best_val = -math.inf
        best_move = (-1, -1)
        for bi in range(9):
            if self.active_board != -1 and not self.is_board_full(self.active_board):
                if bi != self.active_board:
                    continue
            for i in range(9):
                if self.main_board[bi][i] == ' ':
                    temp_board = copy.deepcopy(self.main_board)
                    temp_winners = self.sub_winners[:]
                    temp_board[bi][i] = self.ai_player
                    if self.check_winner(temp_board[bi]) == self.ai_player:
                        temp_winners[bi] = self.ai_player
                    move_val = self.minimax(temp_board, temp_winners, 0, False, i)
                    if move_val > best_val:
                        best_val = move_val
                        best_move = (bi, i)
        return best_move

    def minimax(self, board, winners, depth, is_max, next_active):
        score = self.evaluate(winners)
        if abs(score) == 10 or all(w != ' ' for w in winners) or depth == self.max_depth:
            return score

        if is_max:
            best = -math.inf
            for bi in range(9):
                if next_active != -1 and not self.is_board_full(next_active):
                    if bi != next_active:
                        continue
                for i in range(9):
                    if board[bi][i] == ' ':
                        board[bi][i] = self.ai_player
                        new_winners = winners[:]
                        if self.check_winner(board[bi]) == self.ai_player:
                            new_winners[bi] = self.ai_player
                        val = self.minimax(copy.deepcopy(board), new_winners, depth+1, False, i)
                        best = max(best, val)
                        board[bi][i] = ' '
            return best
        else:
            best = math.inf
            for bi in range(9):
                if next_active != -1 and not self.is_board_full(next_active):
                    if bi != next_active:
                        continue
                for i in range(9):
                    if board[bi][i] == ' ':
                        board[bi][i] = self.human_player
                        new_winners = winners[:]
                        if self.check_winner(board[bi]) == self.human_player:
                            new_winners[bi] = self.human_player
                        val = self.minimax(copy.deepcopy(board), new_winners, depth+1, True, i)
                        best = min(best, val)
                        board[bi][i] = ' '
            return best

    def update_cursor(self):
        cursor_symbol = '➤ X' if self.current_player == 'X' else '➤ O'
        self.cursor_label.config(text=f"Current Turn: {cursor_symbol}")

    def update_button_states(self):
        for bi in range(9):
            if self.active_board == -1:
                self.frames[bi].config(bg='orange')
            elif not self.is_board_full(self.active_board):
                self.frames[bi].config(bg='orange' if bi == self.active_board else 'SystemButtonFace')
            else:
                self.frames[bi].config(bg='orange')

            for i in range(9):
                if self.main_board[bi][i] != ' ':
                    self.buttons[bi][i].config(state='disabled', bg='SystemButtonFace')
                else:
                    if self.active_board == -1:
                        self.buttons[bi][i].config(state='normal', bg='lightyellow')
                    elif not self.is_board_full(self.active_board):
                        if bi == self.active_board:
                            self.buttons[bi][i].config(state='normal', bg='lightyellow')
                        else:
                            self.buttons[bi][i].config(state='disabled', bg='SystemButtonFace')
                    else:
                        self.buttons[bi][i].config(state='normal', bg='lightyellow')

if __name__ == '__main__':
    root = tk.Tk()
    game = GrandTicTacToe(root)
    root.mainloop()
