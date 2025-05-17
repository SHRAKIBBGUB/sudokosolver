# Sudoku Solver - AI Project

## Overview
This project is a graphical Sudoku solver that implements three different artificial intelligence techniques to solve Sudoku puzzles:
1. Backtracking Algorithm
2. Constraint Satisfaction Problem (CSP)
3. Hybrid Approach (Combining CSP and Backtracking)

The application features a user-friendly GUI built with Tkinter that allows users to input puzzles, solve them using different methods, generate random puzzles, and analyze solving statistics.

## Features

### Solving Methods
- **Backtracking**: Classic recursive backtracking algorithm
- **CSP**: Constraint Satisfaction Problem approach with most constrained variable heuristic
- **Hybrid**: Combines CSP for deterministic moves and backtracking for guesses

### User Interface
- Interactive 9x9 Sudoku grid
- Input validation to ensure only valid Sudoku numbers (1-9)
- Visual distinction between 3x3 boxes
- Status bar for operation feedback

### Puzzle Management
- Load default puzzles
- Clear the board
- Generate random puzzles of varying difficulty
- Save puzzles to text files
- Validate puzzle correctness before solving

### Statistics
- Time taken to solve
- Total steps performed
- Backtracking steps count
- CSP steps count
- Number of guesses made

## Requirements
- Python 3.x
- Tkinter (usually included with Python)

## Installation
1. Clone the repository or download the Python file
2. Ensure you have Python 3 installed
3. Run the program with: `python sudoku_solver.py`

## Usage
1. **Input a Puzzle**:
   - Enter numbers directly into the grid
   - Use "Load Default" for a sample puzzle
   - Generate a random puzzle with "Generate Random"

2. **Solve the Puzzle**:
   - Select a solving method (Backtracking, CSP, or Hybrid)
   - Click "Solve" to find the solution
   - View solving statistics in the popup dialog

3. **Validate the Puzzle**:
   - Click "Check" to verify the current puzzle is valid

4. **Save/Load**:
   - Use "Save Puzzle" to save the current state to a text file

## Implementation Details

### Core Algorithms
- **Backtracking**: Standard recursive backtracking with brute-force guessing
- **CSP**: Uses most constrained variable heuristic and least constraining value ordering
- **Hybrid**: Uses CSP for cells with only one possible value, falls back to backtracking

### Heuristics
- **Most Constrained Variable**: Chooses the cell with fewest possible values
- **Least Constraining Value**: Orders possible values by how many constraints they impose

### Board Representation
- 9x9 grid stored as a list of lists
- Empty cells represented by 0

## Examples

### Default Puzzle
The application comes with a built-in default puzzle:

![Image Alt](https://github.com/SHRAKIBBGUB/sudokosolver/blob/main/dp.png?raw=true)


### Random Puzzle Generation
The application can generate puzzles of three difficulty levels:
- Easy: 30-40 empty cells
- Medium: 41-50 empty cells
- Hard: 51-60 empty cells

## Performance Notes
- The hybrid method typically performs best, using CSP where possible and backtracking only when needed
- Backtracking alone can be slow for difficult puzzles
- CSP performs well on puzzles with many constrained cells

## License
This project is open source and available for educational purposes.

## Future Enhancements
- Add puzzle loading from files
- Implement more advanced solving techniques like naked pairs/triples
- Add step-by-step solving visualization
- Include difficulty rating for input puzzles

## Screenshots
(Include screenshots of the application if available)

Enjoy solving Sudoku puzzles with AI techniques!
