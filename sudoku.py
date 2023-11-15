from sys import argv

def main():
    # check for correct input
    if len(argv) != 3:
        print("invalid input")
        return 1

    # open file
    finput = open(argv[1], "r")
    foutput = open(argv[2], "w")

    # load input file into a list called board
    board = load_finput(finput)

    # clone the board to another board that will later be inserted with all possible numbers for every empty cells
    side_board = clone_board(board)

    # put all possible number for every empty cells
    side_board = insert_possible_num(board, side_board)
    
    # use the hidden single technique to solve the cells
    steps = 0
    hidden_single(board, side_board, steps, foutput)

    # close file
    finput.close()
    foutput.close()

    return 0



#load input file into a list
def load_finput(finput):
    board = []
    for lines in finput:
        row = []
        for letter in lines:
            if letter.isalnum() == 1:
                letter = int(letter)
                row.append(letter)
        board.append(row)
    return board

# clone board to make side board and temporary board
def clone_board(board):
    side_board = []
    for row in board:
        side_board.append(row[:])
    return side_board

# put all possible number in a list according to the cell's row, column, and block
def insert_possible_num(board, side_board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                # list of numbers used in the row
                row_val = []
                for val in board[row]:
                    if val != 0:
                        row_val.append(val)
                
                #list of numbers used in the column
                col_val = []
                for i in range(9):
                    if board[i][col] != 0:
                        col_val.append(board[i][col])
                
                # list of numbers used in the block
                block_row, block_col = 3 * (row // 3), 3 * (col // 3)
                block_val = []
                for i in range(3):
                    for j in range(3):
                        if board[block_row + i][block_col + j] != 0:
                            block_val.append(board[block_row + i][block_col + j])
                
                # possible numbers = numbers one to 9 - used numbers
                used_val = row_val + col_val + block_val
                used_val = [i for n, i in enumerate(used_val) if i not in used_val[:n]]
                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for num in used_val:
                    if num in numbers:
                        numbers.remove(num)
                side_board[row][col] = numbers

    return side_board

# compare previous side_board with current side_board after solving
def compare_side_board(side_board, temp_board):
    if len(side_board) != len(temp_board):
        return False

    for i in range(len(side_board)):
        if len(side_board[i]) != len(temp_board[i]):
            return False

        for j in range(len(side_board[i])):
            if side_board[i][j] != temp_board[i][j]:
                return False

    return True

# use the hidden single technique to solve the cells. returns the new updated table
def hidden_single(board, side_board, steps, foutput):
    temp_board = clone_board(side_board)

    for row in range(9):
        for col in range(9):
            if type(side_board[row][col]) == list:
                if len(side_board[row][col]) == 1:
                    steps = steps + 1
                    side_board[row][col] = side_board[row][col][0]
                    board[row][col] = side_board[row][col]
                    print_table(steps, board, row, col, foutput)

                    # update the side board after solving a cell
                    side_board = insert_possible_num(board, side_board)
    
                    # compare the previous board with the new updated board
                    if compare_side_board(side_board, temp_board) == False:
                        hidden_single(board, side_board, steps, foutput)

    return 0

# print table into output file
def print_table(steps, board, row, col, foutput):
    heading = ["Step " + str(steps) + " - " + str(board[row][col]) + " @ R" + str(row + 1) + "C" + str(col + 1)]
    strips = ["-"*18]
    
    foutput.write(heading[0] + "\n")
    foutput.write(strips[0] + "\n")
    for r in board:
                foutput.write(" ".join(map(str, r)) + "\n")
    foutput.write(strips[0] + "\n")

    return 0

main()