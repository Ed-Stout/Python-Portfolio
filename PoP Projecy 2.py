# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 22:18:01 2025

@author: eddie
"""
import os

import random

#It will be convenient, instead of using chess locations given by columns and rows, such as e2, to use the horizontal (i.e., x) and vertical (i.e., y) coordinates of a location ranging from 1 to 26, 
#such as, respectively, 5 and 2. The column a corresponds to the horizontal coordinate 1, the column b corresponds to the horizontal coordiate 2, etc., while row 1 corresponds to the vertical coordinate 1,
#row 2 corresponds to the vertical coordinate 2, etc. We need a function that converts chess locations to coordinates, and another function that converts vice versa:

def location2index(loc: str) -> tuple[int, int]: #local - it will not contain the piece name
    '''converts chess location to corresponding x and y coordinates''' #e.g. BA12 = [1, 12]
    if len(loc) < 2 or len(loc) > 3 or not loc[0].isalpha() or not loc[1:].isdigit():
        raise ValueError("Invalid location format")
    loc_split = loc[1:] # split before the second chracter - assumes location given contains the piece name
    row_num = ord(loc_split[0].upper()) - 64 #turns the letter into the corresponding number e.g. A -> 1. 64 is removed bc of unicode numbering
    col_num = int(loc_split[1:]) #second half of the split e.g. anything after alpha 
    return (row_num, col_num)
    
def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
    row_loc = chr(x + 64) #converts to letter 
    loc = row_loc + str(y)
    return (loc)

"""def piece2str(Piece) -> str:
    board_size, board_list = Board
    for i in board_list:
        i[0] = colour
        if colour.upper() == "W"
            return True
        elif colour.upper() == "B"
            return False"""

def split_move(whitemove: str) -> tuple[str, str]:
    for i in range(len(white_move)):
        if whitemove[i].isalpha(): 
            return whitemove[:i], whitemove[i:]

class Piece:
    pos_x : int	
    pos_y : int
    side : bool #True for White and False for Black
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values'''
        self.pos_X = pos_X
        self.pos_Y = pos_Y
        self.side_ = side_
        self.type = self.__class__.__name__[0] #B, K

Board = tuple[int, list[Piece]] #e.g. (5, [bb1, bk1, wb1, wk1]), Bishop(3, 4, True)

#and to represent a board configuration, we will use a pair (tuple) of an integer representing the size of the board S and a list of pieces, i.e.,

#The list of pieces contains all the pieces present on the board and the locations on the board with the coordinates not occupied by any piece in the list are considered empty. The following two functions are required:
def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    '''checks if there is piece at coordinates pox_X, pos_Y of board B''' 
    return any(pos_X == board_x and pos_Y == board_y for piece in B[1]) #any() gives a boolean
	
def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B 
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    '''
    board_location, board_list_temp = Board

    for piece in board_list_temp: #iterate over all items in Board_list #Get the first two characters from Board list e.g. Bishop(3, 4, True) -> 3, 4
        if piece.pos_x == pos_x and piece.pos_y == pos_Y:
            return piece

class Bishop(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_) #Week 8 video
	
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] (see section Intro)
        Hint: use is_piece_at
        '''
        #[Rule1] A bishop can move any number of squares diagonally, but cannot leap over other pieces.
        #[Rule3] A piece of side X (Black or White) cannot move to a location occupied by a piece of side X.
        #Week 6 video

        if abs(pos_X - self.pos_X) != abs(pos_Y - self.pos_Y):
            return False #not diagonal
        
        move_X = 1 if pos_X > self.pos_X else -1 #direction of x - if higher then 1, lower -1. Can't be the same as diagnoal means both always change
        move_Y = 1 if pos_Y > self.pos_Y else -1 #same for y
        
        inbetween_X = self.pos_X + move_X #start the move
        inbetween_Y = self.pos_Y + move_Y

        while (inbetween_X, inbetween_Y) != (pos_X, pos_Y): #check piece isn't on loc
            if is_piece_at(x, y, B): #check no piece
                return False
            inbetween_X += move_X
            inbetween_Y += move_Y

        if is_piece_at(pos_X, pos_Y, B):
            move_piece = piece_at(pos_X, pos_Y, B)
            if move_piece.side_ == self.side_:
                return False #blocked by same side

        return True
        

    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        
        Hints:
        - firstly, check [Rule1] and [Rule3] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule4], use is_check on new board
        '''
        cmt_new_board = []

        if self.can_reach(pos_X, pos_Y, B) == False: #rule1 and rule3
            return False

        taken_piece = None
        if is_piece_at(pos_X, pos_Y, B): #if there is, then it has to . Also no need to put == True
            if piece_at(pos_X, pos_Y, B).side_ != self.side_:  #need to check if it's not the same type, otherwise return False
                taken_piece = piece_at(pos_X, pos_Y, B)
            else:
                return False

        for i in B[1]: #add every piece other than the current bishop to the new board
            if i != self and i != taken_piece:
                cmt_new_board.append(i)
        
        cmt_new_board.append(Bishop(pos_X, pos_Y, self.side_))
        new_board = (B[0], cmt_new_board) #Board_size remains the same

        if is_check(self.side_, new_board): #Can't move a piece in such a way that causes a check
            return False
        
        return True
        
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        if self.can_move_to(pos_X, pos_Y, B) == False:
            raise ValueError("invalid move")
        
        taken_piece = None
        if is_piece_at(pos_X, pos_Y, B): #if there is, then it has to . Also no need to put == True
            taken_piece = piece_at(pos_X, pos_Y, B)

        cmt_new_board = []
        for i in B[1]: #add every piece other than the current bishop to the new board
            if i != self and i != taken_piece:
                cmt_new_board.append(i)
        
        cmt_new_board.append(Bishop(pos_X, pos_Y, self.side_))
        
        return (B[0], cmt_new_board)

    def __str__(self, B: Board) -> str:
        board_size, board_list = B
        
        piece_colour = str()    
        piece_type =self.type
        p_num = 1

        if self.side_ == True:  #W, W
            piece_colour = "W"
        elif self.side_ == False:
            piece_colour = "B"
        
        piece_index = 0
        for piece in board_list:
            if piece.type == self.type and piece.side_ == self.side_: #how many before this one
                piece_index += 1
            if piece == self:
                p_num = piece_index #give the piece p_num
                break

        return str(piece_colour) + "b" + str(p_num)

class King(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_) #Week 8 video

    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule2] and [Rule3]'''

        #do we need something to check if the move is out of bounds?

        if abs(self.pos_X - pos_X) > 1 or abs(self.pos_Y - pos_Y) > 1:
            return False

        if is_piece_at(pos_X, pos_Y, B) == True and piece_at(pos_X, pos_Y, B).side_ == self.side_: #blocked
            return False

        return True

    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''

        cmt_new_board = []

        if self.can_reach(pos_X, pos_Y, B) == False: #rule1 and rule3
            return False
        
        if pos_X < 1 or pos_X > 26 or pos_Y < 1 or pos_Y > 26: #checking length of inputs
            raise ValueError("Co-ordinates must be between 1 and 26")
            return False
        
        taken_piece = None
        if is_piece_at(pos_X, pos_Y, B): #if there is, then it has to . Also no need to put == True
            if piece_at(pos_X, pos_Y, B).side_ != self.side_:  #need to check if it's not the same type, otherwise return False
                taken_piece = piece_at(pos_X, pos_Y, B)
            else:
                return False

        for i in B[1]: #add every piece other than the current king to the new board
            if i != self and i != taken_piece:
                cmt_new_board.append(i)
        
        cmt_new_board.append(King(pos_X, pos_Y, self.side_))
        new_board = (B[0], cmt_new_board) #Board_size remains the same

        if is_check(self.side_, new_board): #Can't move a piece in such a way that causes a check
            return False
        
        return True

    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        if self.can_move_to(pos_X, pos_Y, B) == False:
            raise ValueError("invalid move")
        
        taken_piece = None
        if is_piece_at(pos_X, pos_Y, B): #if there is, then it has to . Also no need to put == True
            taken_piece = piece_at(pos_X, pos_Y, B)

        cmt_new_board = []
        for i in B[1]: #add every piece other than the current bishop to the new board
            if i != self and i != taken_piece:
                cmt_new_board.append(i)
        
        cmt_new_board.append(King(pos_X, pos_Y, self.side_))
        
        return (B[0], cmt_new_board)

    def __str__(self, B: Board) -> str:
        board_size, board_list = B
        
        piece_colour = str()    
        piece_type = self.type
        p_num = 1

        if self.side_ == True:  #W, W
            piece_colour = "W"
        elif self.side_ == False:
            piece_colour = "B"
        
        piece_index = 0
        for piece in board_list:
            if piece.type == self.type and piece.side_ == self.side_: #how many before this one
                piece_index += 1
            if piece == self:
                p_num = piece_index #give the piece p_num
                break
        
        return str(piece_colour) + "k" + str(p_num)

#To check for checks and checkmates, we require the functions:
def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    '''
    #take the two king poistions, and iterate through the board
    #if any piece can_reach == True, return True
    big_k = None
    for piece in B[1]:
        if isinstance(piece, King) and piece.side_ == side:
            big_k = piece
            break
        
    for piece in B[1]:
        if side != piece.side_ and piece.can_reach(big_k.pos_X, big_k.pos_Y, B):
            return True

    return False

def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side

    Hints: 
    - use is_check
    - use can_move_to
    '''
    if not is_check(side, B):
        return False

    for piece in B[1]:
        if isinstance(piece, King) and piece.side_ == side:
            big_k = piece
            break
    
    board_size, board_list = B

    #do we need to check if moves are in bounds?

    for x in range(-1, 2): #left, right, the same     #iterates through, finds a move that works
        for y in range(-1, 2): #up, down, the same
            if x == 0 and y == 0: #has to move, in check
                continue

            move_x = big_k.pos_X + x
            move_y = big_k.pos_Y + y

            if big_k.can_move_to(move_x, move_y, B): #if it can move to these places
                checkmate_board = big_k.move_to(move_x, move_y, B)
                if is_check(side, checkmate_board) == False: 
                    return False

    return True
    
def is_stalemate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is stalemate for side

    Hints: 
    - use is_check
    - use can_move_to 
    '''
    if is_check(side, B):
        return False
    
    for piece in B[1]:
        if piece.side_ == side:
            board_size, board_list = B
            for x in range(1, board_size + 1): #start at 1
                for y in range(1, board_size + 1):
                    if piece.can_move_to(x, y, B): #if the piece can move then it's not a stalemate. Could use this logic for checkmate
                        return False
    
    return True

#To read the configuration from files (on PC) and save it, we will need the functions:
def read_board(filename: str) -> Board:
    '''
    Reads board configuration from a file with flexible line handling.
    Raises IOError if the essential format is invalid.
    '''
    try:
        with open(filename, "r") as b_file:
            # Read all lines and strip whitespace, ignore empty and comment lines
            boardlines = [line.strip() for line in b_file if line.strip() and not line.strip().startswith("#")]

        # Validate minimum line count
        if len(boardlines) < 3:
            raise IOError("File must have at least three non-empty, non-comment lines (size, white pieces, black pieces).")

        # Extract and validate board size
        board_size_line = boardlines[0]
        if not board_size_line.isdigit():
            raise ValueError(f"The first valid line must be an integer for the board size. Found: '{board_size_line}'")
        
        board_size = int(board_size_line)

        # Parse white and black pieces
        white_pieces_line = boardlines[1]
        black_pieces_line = boardlines[2]

        white_pieces = [piece.strip() for piece in white_pieces_line.split(",") if piece.strip()]
        black_pieces = [piece.strip() for piece in black_pieces_line.split(",") if piece.strip()]

        print(f"Board size: {board_size}")
        print(f"White pieces: {white_pieces}")
        print(f"Black pieces: {black_pieces}")

        board_list = []

        # Parse pieces
        for piece in white_pieces + black_pieces:
            if len(piece) < 3:
                raise ValueError(f"Invalid piece format: {piece}")

            piece_type = piece[0]
            piece_loc = piece[1:]

            if piece_type not in ("B", "K"):
                raise ValueError(f"Invalid piece type: {piece_type}")

            pos_x, pos_y = location2index(piece_loc)
            side = piece in white_pieces

            if piece_type == "B":
                board_list.append(Bishop(pos_x, pos_y, side))
            elif piece_type == "K":
                board_list.append(King(pos_x, pos_y, side))

        return (board_size, board_list)

    except Exception as e:
        print(f"Error in read_board: {e}")
        raise IOError("Failed to parse the board configuration file.")


def save_board(filename: str, B: Board) -> None:
    '''Saves board configuration into a file in the current directory in plain format.'''

    board_size, board_list = B

    white_pieces = []
    black_pieces = []

    # Categorize pieces
    for piece in board_list:
        b_k = "B" if isinstance(piece, Bishop) else "K"
        b_location = index2location(piece.pos_X, piece.pos_Y)
        save_piece_name = b_k + b_location

        if piece.side_:
            white_pieces.append(save_piece_name)
        else:
            black_pieces.append(save_piece_name)

    # Write to file
    try:
        with open(filename, 'w') as f:
            f.write(f"{board_size}\n")
            if white_pieces:
                f.write(", ".join(white_pieces) + "\n")
            if black_pieces:
                f.write(", ".join(black_pieces) + "\n")
            f.write("\n")  # Ensure final newline
    except IOError:
        print(f"Error: Unable to write to file '{filename}'")

            

#To generate Black’s moves by the computer player, we need:
#We suggest the following simplest approach to implement find_black_move. For every Black piece on the board and piece coordinates x,y, where x and y are in the range 1..S, check if the piece can move there. 
#If so, return this piece and the coordinates. Further, to make the behaviour of the computer player less "predictable", you can pick the pieces on the board in a random order. 
#Also, you can pick the coordinates randomly. This function will not be verified by unit tests (see next section) and you can use any approach to implement it that returns valid results.
def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assumes there is at least one black piece that can move somewhere

    Hints: 
    - use methods of random library
    - use can_move_to
    '''

    board_size, board_list = B
    black_pieces = []

    for piece in board_list:
        if not piece.side_:
            black_pieces.append(piece)

    possible_moves = [(x, y) for x in range(1, board_size + 1) for y in range(1, board_size + 1)] #The function randint takes parameters low and high and returns an integer between low and high (including both).


    random.shuffle(black_pieces)
    random.shuffle(possible_moves)

    for piece in black_pieces: 
        for (x, y) in possible_moves:
            if piece.can_move_to(x, y, B): 
                return (piece, x, y)              

#For the screen output, we need: #Board = tuple[int, list[Piece]] Need to link to Piece as board only stores pieces, but not which piece is which
def conf2unicode(B: Board) -> str: 
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''
    
    board_size, board_pieces = B

    temp_board = [] #[(1,1), (1,2)]

    for row in range(board_size, 0, -1): #(1,2,3)
        temp_row = str()
        for col in range(1, board_size + 1): #(1,2,3)

            if is_piece_at(col, row, B) == True:
                conf_piece = piece_at(col, row, B)
                if type(conf_piece) == Bishop:
                    if conf_piece.side_ == False: #W
                        temp_row += "\u265D" #Black bishop
                    elif conf_piece.side_ == True:
                        temp_row += "\u2657" #White bishop
                elif type(conf_piece) == King:
                    if conf_piece.side_ == False:
                        temp_row += "\u265A" #Black king
                    elif conf_piece.side_ == True:
                        temp_row += "\u2654" #White king

            elif is_piece_at(col, row, B) == False:
                temp_row += "\u2001" #Space
        
        temp_board.append(temp_row) #add row to board

    final_board = str() #need long string
    for i in range(len(temp_board)):
        final_board += temp_board[i]
        if i < len(temp_board) - 1:
            final_board += "\n"

    return final_board


def main() -> None:
    '''
    Runs the play with improved file handling using `os.path`.
    '''

    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Prompt user for file input
    while True:
        filename = input("File name for initial configuration: ").strip()

        if filename.upper() == "QUIT":
            print("Quitting the game.")
            return

        # Combine user input with script directory to get absolute path
        full_path = os.path.join(script_dir, filename)

        if os.path.exists(full_path):
            try:
                Board = read_board(full_path)
                break  # Exit the loop if file is valid
            except IOError:
                print("Error: The file could not be read. Try again or type QUIT to exit.")
        else:
            print(f"Error: The file '{filename}' does not exist in the script directory ({script_dir}).")
            print("Please try again or type QUIT to exit.")
            
    print("The initial configuration is:")
    print(conf2unicode(Board))        

    game_bool = True
    #Moves
    while game_bool:   
        white_move_bool = False  
        whitemove = None

        while not white_move_bool:
            if whitemove == None:
                whitemove = input("Next move of White: ")

            if whitemove == "QUIT":
                save_file = input("File name to store the configuration: ")
                if save_board(save_file, Board):
                    print("The game configuration saved.")
                game_bool = False
            
            #here we have an issue. If we have an issue with whitemove and output ("This is not a valid move. Next move of White: ") When we redo the loop, it keeps going round
            start_loc, end_loc = split_move(whitemove)
            start_x, start_y = location2index(start_loc)
            end_x, end_y = location2index(end_loc)

            piece = piece_at(start_x, start_y, Board)
            if piece.side_ and piece.can_move_to(end_x, end_y, Board): #check piece can move and is correct side
                Board = piece.move_to(end_x, end_y, Board)
                print("The configuration after White's move is:")
                print(conf2unicode(Board))

                if is_checkmate(False, Board): #check that this is the correct side - should the input be for the side that is playing
                    print("Game over. White wins.")
                    game_bool = False
                
                if is_stalemate(False, Board):
                    print("Game over. Stalemate.")
                    game_bool = False
                
                white_move_bool = True #exit loop
                whitemove = None #reset
            elif not piece.can_move_to(end_x, end_y, Board): #is this okay? Doesn't include the side parameter
                whitemove = input("This is not a valid move. Next move of White: ")
                break

        black_piece, black_move_x, black_move_y = find_black_move(Board)

        start_black_loc = index2location(black_piece.pos_X, black_piece.pos_Y)
        end_black_loc = index2location(black_move_x, black_move_y)

        black_move_string = start_black_loc + end_black_loc

        print("Next move of Black is " + black_move_string + ". The configuration after Black's move is:")
        print(conf2unicode(Board))

        if is_checkmate(True, Board):
            print("Game over. Black wins.")
            game_bool = False
        
        if is_stalemate(True, Board):
            print("Game over. Stalemate.")
            game_bool = False




    

if __name__ == '__main__': #keep this in
   main()
