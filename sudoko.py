import tkinter as tk
from tkinter import messagebox, filedialog
import time
import copy
import random

class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.initial_board = copy.deepcopy(board)
        self.reset_stats()
    
    def reset_stats(self):
        self.total_steps = 0
        self.backtracking_steps = 0
        self.csp_steps = 0
        self.guesses = 0
    
    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def is_valid(self, num, pos):
        row, col = pos
        
        if num in self.board[row]:
            return False
            
        if num in [self.board[i][col] for i in range(9)]:
            return False
            
        box_x = col // 3
        box_y = row // 3
        for i in range(box_y*3, box_y*3+3):
            for j in range(box_x*3, box_x*3+3):
                if self.board[i][j] == num:
                    return False
        return True
    
    def get_possible_values(self, pos):
        possible = []
        for num in range(1, 10):
            if self.is_valid(num, pos):
                possible.append(num)
        return possible
    
    def solve_backtracking(self):
        self.total_steps += 1
        empty = self.find_empty()
        
        if not empty:
            return True
            
        row, col = empty
        
        for num in range(1, 10):
            self.backtracking_steps += 1
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                
                if self.solve_backtracking():
                    return True
                    
                self.board[row][col] = 0
                self.guesses += 1
                
        return False
    
    def solve_csp(self):
        self.total_steps += 1
        
        empty = self.find_most_constrained_cell()
        if not empty:
            return True
            
        row, col = empty
        possible_values = self.get_possible_values((row, col))
        
        if not possible_values:
            return False
            
        for num in sorted(possible_values, key=lambda x: self.count_constraints(x, (row, col))):
            self.csp_steps += 1
            self.board[row][col] = num
            
            if self.solve_csp():
                return True
                
            self.board[row][col] = 0
            self.guesses += 1
            
        return False
    
    def solve_hybrid(self):
        self.total_steps += 1
        
        empty = self.find_most_constrained_cell()
        if not empty:
            return True
            
        row, col = empty
        possible_values = self.get_possible_values((row, col))
        
        if not possible_values:
            return False
            
        if len(possible_values) == 1:
            self.csp_steps += 1
            self.board[row][col] = possible_values[0]
            return self.solve_hybrid()
        
        for num in sorted(possible_values, key=lambda x: self.count_constraints(x, (row, col))):
            self.backtracking_steps += 1
            self.board[row][col] = num
            
            if self.solve_hybrid():
                return True
                
            self.board[row][col] = 0
            self.guesses += 1
            
        return False
    
    def find_most_constrained_cell(self):
        min_possibilities = 10
        best_cell = None
        
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    possibilities = len(self.get_possible_values((i, j)))
                    if possibilities < min_possibilities:
                        min_possibilities = possibilities
                        best_cell = (i, j)
                        if min_possibilities == 1:
                            return best_cell
        return best_cell
    
    def count_constraints(self, num, pos):
        count = 0
        row, col = pos
        
        for j in range(9):
            if self.board[row][j] == 0 and j != col and not self.is_valid(num, (row, j)):
                count += 1
                
        for i in range(9):
            if self.board[i][col] == 0 and i != row and not self.is_valid(num, (i, col)):
                count += 1
                
        box_x = col // 3
        box_y = row // 3
        for i in range(box_y*3, box_y*3+3):
            for j in range(box_x*3, box_x*3+3):
                if self.board[i][j] == 0 and (i,j) != pos and not self.is_valid(num, (i, j)):
                    count += 1
                    
        return count
    
    def validate_board(self):
        for i in range(9):
            row = [num for num in self.initial_board[i] if num != 0]
            if len(row) != len(set(row)):
                return False, f"Duplicate in row {i+1}"
        
        for j in range(9):
            col = [self.initial_board[i][j] for i in range(9) if self.initial_board[i][j] != 0]
            if len(col) != len(set(col)):
                return False, f"Duplicate in column {j+1}"
        
        for box_y in range(3):
            for box_x in range(3):
                box = []
                for i in range(box_y*3, box_y*3+3):
                    for j in range(box_x*3, box_x*3+3):
                        if self.initial_board[i][j] != 0:
                            box.append(self.initial_board[i][j])
                if len(box) != len(set(box)):
                    return False, f"Duplicate in box ({box_y+1}, {box_x+1})"
        return True, "Valid board"
    
    def reset_board(self):
        self.board = copy.deepcopy(self.initial_board)
        self.reset_stats()

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("600x700")
        
        self.solver = None
        self.cells = {}
        self.method_var = tk.StringVar(value="hybrid")
        
        # Store the default board
        self.default_board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        
        self.create_menu()
        self.create_controls()
        self.create_board()
        self.create_status_bar()
        
        self.load_default_board()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Puzzle", command=self.clear_board)
        file_menu.add_command(label="Save Puzzle", command=self.save_puzzle)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        method_frame = tk.LabelFrame(control_frame, text="Solving Method")
        method_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(method_frame, text="Backtracking", variable=self.method_var, value="backtracking").pack(anchor=tk.W)
        tk.Radiobutton(method_frame, text="CSP", variable=self.method_var, value="csp").pack(anchor=tk.W)
        tk.Radiobutton(method_frame, text="Hybrid", variable=self.method_var, value="hybrid").pack(anchor=tk.W)
        
        button_frame = tk.Frame(control_frame)
        button_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Solve", command=self.solve_board, width=10).pack(pady=5)
        tk.Button(button_frame, text="Clear", command=self.clear_board, width=10).pack(pady=5)
        tk.Button(button_frame, text="Check", command=self.validate_board, width=10).pack(pady=5)
        tk.Button(button_frame, text="Load Default", command=self.load_default_board, width=10).pack(pady=5)
        
        button_frame2 = tk.Frame(control_frame)
        button_frame2.pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame2, text="Generate Random", command=self.generate_random_puzzle, width=16).pack(pady=5)
    
    def create_board(self):
        board_frame = tk.Frame(self.root)
        board_frame.pack(pady=10)
        
        for row in range(9):
            for col in range(9):
                border_width = 1
                if row % 3 == 0:
                    border_width = 2
                if col % 3 == 0:
                    border_width = 2
                
                cell = tk.Entry(
                    board_frame,
                    width=3,
                    font=('Arial', 18),
                    justify='center',
                    borderwidth=border_width,
                    relief='solid'
                )
                cell.grid(row=row, column=col, ipady=5)
                
                cell['validate'] = 'key'
                cell['validatecommand'] = (cell.register(self.validate_input), '%P')
                
                self.cells[(row, col)] = cell
    
    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def validate_input(self, new_value):
        return new_value == "" or (new_value.isdigit() and 1 <= int(new_value) <= 9)
    
    def get_board_from_gui(self):
        board = []
        for row in range(9):
            board_row = []
            for col in range(9):
                value = self.cells[(row, col)].get()
                board_row.append(int(value) if value else 0)
            board.append(board_row)
        return board
    
    def set_board_to_gui(self, board):
        for row in range(9):
            for col in range(9):
                value = board[row][col]
                self.cells[(row, col)].delete(0, tk.END)
                if value != 0:
                    self.cells[(row, col)].insert(0, str(value))
    
    def load_default_board(self):
        """Load the default Sudoku puzzle"""
        self.set_board_to_gui(self.default_board)
        self.status_var.set("Default puzzle loaded")
    
    def clear_board(self):
        for row in range(9):
            for col in range(9):
                self.cells[(row, col)].delete(0, tk.END)
        self.status_var.set("Board cleared")
    
    def validate_board(self):
        board = self.get_board_from_gui()
        self.solver = SudokuSolver(board)
        valid, message = self.solver.validate_board()
        
        if valid:
            messagebox.showinfo("Validation", "The Sudoku puzzle is valid!")
            self.status_var.set("Puzzle is valid")
        else:
            messagebox.showerror("Validation Error", message)
            self.status_var.set(message)
    
    def solve_board(self):
        board = self.get_board_from_gui()
        self.solver = SudokuSolver(board)
        
        valid, message = self.solver.validate_board()
        if not valid:
            messagebox.showerror("Validation Error", message)
            self.status_var.set(message)
            return
        
        method = self.method_var.get()
        start_time = time.time()
        
        if method == "backtracking":
            solved = self.solver.solve_backtracking()
        elif method == "csp":
            solved = self.solver.solve_csp()
        else:
            solved = self.solver.solve_hybrid()
        
        time_taken = time.time() - start_time
        
        if solved:
            self.set_board_to_gui(self.solver.board)
            stats = (
                f"Solved with {method.capitalize()}!\n"
                f"Time: {time_taken:.3f} seconds\n"
                f"Total steps: {self.solver.total_steps}\n"
                f"Backtracking steps: {self.solver.backtracking_steps}\n"
                f"CSP steps: {self.solver.csp_steps}\n"
                f"Guesses made: {self.solver.guesses}"
            )
            messagebox.showinfo("Solution Found", stats)
            self.status_var.set(f"Solved with {method} in {time_taken:.2f}s")
        else:
            messagebox.showerror("No Solution", "The Sudoku puzzle has no solution!")
            self.status_var.set("No solution exists")
    
    def generate_random_puzzle(self):
        solved_board = self.generate_solved_sudoku()
        
        difficulty = random.choice(["easy", "medium", "hard"])
        
        if difficulty == "easy":
            cells_to_remove = random.randint(30, 40)
        elif difficulty == "medium":
            cells_to_remove = random.randint(41, 50)
        else:
            cells_to_remove = random.randint(51, 60)
        
        puzzle_board = copy.deepcopy(solved_board)
        
        removed = 0
        while removed < cells_to_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if puzzle_board[row][col] != 0:
                puzzle_board[row][col] = 0
                removed += 1
        
        self.set_board_to_gui(puzzle_board)
        self.status_var.set(f"Generated {difficulty} puzzle with {cells_to_remove} empty cells")
    
    def generate_solved_sudoku(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        
        for box in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for i in range(3):
                for j in range(3):
                    board[box + i][box + j] = nums.pop()
        
        solver = SudokuSolver(board)
        if solver.solve_hybrid():
            return solver.board
        else:
            return self.generate_solved_sudoku()
    
    def save_puzzle(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Sudoku Puzzle",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            board = self.get_board_from_gui()
            with open(file_path, 'w') as f:
                for row in board:
                    f.write(" ".join(str(num) if num != 0 else "." for num in row) + "\n")
            
            self.status_var.set(f"Puzzle saved to {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save puzzle:\n{str(e)}")
    
    def show_about(self):
        about_text = (
            "Sudoku Solver - AI Project\n"
            "Implemented Techniques:\n"
            "- Backtracking Algorithm\n"
            "- Constraint Satisfaction Problem (CSP)\n"
            "- Hybrid Approach (CSP + Backtracking)\n\n"
            "Developed as part of CSE-316: Artificial Intelligence Lab"
        )
        messagebox.showinfo("About", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()