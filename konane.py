'''
Game board class
'''


class Board:
    def __init__(self, width):
        self.width = width
        self.board = [[' ' for col in range(self.width + 1)] for row in range(self.width + 1)];  # 2D arr

    "initiate 8x8 board, 1 black, 0 white"

    def create_board(self, width):
        for row in range(self.width + 1):
            for col in range(self.width + 1):
                if (row == 0):
                    self.board[row][col] = col;  # put index
                    self.board[row][0] = ' '

                elif (col == 0):
                    self.board[row][col] = row

                elif ((row + col) % 2 == 0):
                    self.board[row][col] = '1'

                else:
                    self.board[row][col] = '0'

        return self.board

    def print_board(self, board):
        for row in range(self.width + 1):
            for col in range(self.width + 1):
                print(board[row][col]),
            print

    def get_piece(self, x, y):
        if self.out_of_bound(x, y):
            # print("not valid coordinate")
            # raise Exception('coordinate not in range')
            pass
        else:
            return self.board[y][x]

    def get_one_piece_movable(self, x, y):
        movable = []
        if self.out_of_bound(x, y) or self.get_piece(x,y) is ' ':
            print("not valid coordinate")
            raise Exception('coordinate not in range')
        if self.is_initial():
            #print('this is inital')
            if (x, y) == (8, 8) or (x, y) == (1, 1) or (x, y) ==(4, 4) or (x, y) == (5, 5):
                movable.append((0, 0))
            return movable

        if self.is_second():
            #print('this is second')
            thisx = 0
            thisy = 0
            for row in range(self.width + 1):
                for col in range(self.width + 1):
                    if self.board[row][col] == ' ':
                        thisx = col
                        thisy = row
            if (x,y) == (thisx+1,thisy) or (x,y) == (thisx-1,thisy) or (x,y) == (thisx,thisy+1) or (x,y) == (thisx,thisy-1):
                movable.append((0, 0))
            return movable

        else:
            if self.check_movable(x,y,x+2,y,self.get_piece(x,y)):
                movable.append((x + 2, y))

            if self.check_movable(x,y,x-2,y,self.get_piece(x,y)):
                movable.append((x - 2, y))

            if self.check_movable(x,y,x,y+2,self.get_piece(x,y)):
                movable.append((x , y + 2))

            if self.check_movable(x,y,x,y-2,self.get_piece(x,y)):
                movable.append((x, y - 2))
            newmovable = []
            for corr in movable:
                newmovable = self.recursive_move_helper(corr[0], corr[1], movable,x,y)

        return newmovable

    def get_possible_move(self,color):
        movable = []
        for row in range(1,self.width + 1):
            for col in range(1,self.width + 1):

                if self.get_piece(row,col) == color:
                    moves = self.get_one_piece_movable(row, col)
                    if len(moves)!=0:
                        movable.append(((row,col),moves))
        return movable
    '''generate the next board with the color, from coordinate and to coordinate'''
    def next_board(self,fromx,fromy,tox,toy,color):

        self.board_remove(fromx, fromy)

        if tox!=0: #means not removing the piece (at the first move you remove the piece)

            self.board_add(tox,toy,color)



    def get_all_next_boards(self, color):
        moves = self.get_possible_move(color)
        boards = []
        for pair in moves:
            for des in pair[1]:
                boards.append(self.get_next_board(pair[0][0],pair[0][1],des[0],des[1],color))

        return boards

    '''get a random move from the movable list and generate the next board'''
    def random_move(self,color):
        import random
        moves = self.get_possible_move(color)
        if len(moves)==0:
            return None
        piece = random.choice(moves)
        move = random.choice(piece[1])
        self.next_board(piece[0][0],piece[0][1],move[0],move[1],color)
        return (piece[0][0],piece[0][1],move[0],move[1])


    def check_lost(self,color):
        if len(self.get_possible_move(color))==0:
            return True
        return  False
    ##helper method##
    """check if the position x,y movable to tox, tox given a specific color"""

    def board_remove(self,x,y):
        self.board[y][x] = ' '

    def board_add(self,x,y,color):
        self.board[y][x] = color
    def check_movable(self, x, y, tox, toy, color):
        if color == '1': #change this color to oppo side, to check if the intermediate piece is of that color
            color = '0'
        else:
            color = '1'
        if x != tox:
            return self.get_piece((tox + x) / 2, toy) is color and not self.out_of_bound(tox, y) and self.get_piece(tox, y) is ' '
        elif y != toy:
            return self.get_piece(x, (toy+y)/2) is color and not self.out_of_bound(x, toy) and self.get_piece(x, toy) is ' '
        return False

    def get_possible_move_num(self,color):
        moves = self.get_possible_move(color)
        count = 0
        for pair in moves:
            count += len(pair[1])

        return count


    '''helper method to recursively find the mult step jump
    :parameter ox: original x of the piece  oy: original y of the piece, movable set of the piece, x,y is the coordinate we want to explore'''
    def recursive_move_helper(self, x, y, movable,ox,oy):
        if self.check_movable(x, y, x + 2, y,self.get_piece(ox,oy)):
            if movable.count((x+2,y))==0 and (x+2,y) is not (ox,oy):
                movable.append((x+2,y))
                return self.recursive_move_helper(x+2,y,movable,ox,oy)

        if self.check_movable(x, y, x - 2, y, self.get_piece(ox,oy)):
            if movable.count((x-2,y))==0 and (x-2,y) is not (ox,oy):
                movable.append((x-2,y))
                return self.recursive_move_helper(x-2,y,movable,ox,oy)

        if self.check_movable(x, y, x, y + 2, self.get_piece(ox,oy)):
            if movable.count((x,y+2))==0 and (x,y+2) is not (ox,oy):
                movable.append((x,y+2))
                return self.recursive_move_helper(x,y+2,movable,ox,oy)

        if self.check_movable(x, y, x, y - 2, self.get_piece(ox,oy)):
            if movable.count((x,y-2))==0 and (x,y-2) is not (ox,oy):
                movable.append((x,y-2))
                return self.recursive_move_helper(x,y-2,movable,ox,oy)

        return movable

    def get_all_actions(self,color):
        moves = self.get_possible_move(color)
        actions = []
        for pair in moves:
            for des in pair[1]:
                actions.append((pair[0][0],pair[0][1],des[0],des[1]))

        return actions

    def get_next_board(self,fromx,fromy,tox,toy,color):
        import copy
        c = copy.deepcopy(self)
        c.board_remove(fromx, fromy)

        if tox!=0: #means not removing the piece (at the first move you remove the piece)

            c.board_add(tox,toy,color)

        return c

    def out_of_bound(self, x, y):
        if x > self.width or y > self.width or x == 0 or y == 0:
            return True
        return False

    def is_initial(self):
        for row in range(self.width + 1):
            for col in range(self.width + 1):
                if (row == 0):
                    pass

                elif (col == 0):
                    pass

                elif ((row + col) % 2 == 0):
                    if self.board[row][col] != '1':
                        return False

                else:
                    if self.board[row][col] != '0':
                        return False

        return True

    def is_second(self):
        if board.is_initial():
            return False
        for row in range(self.width + 1):
            for col in range(self.width + 1):
                if (row == 0):
                    pass

                elif (col == 0):
                    pass

                elif ((row + col) % 2 == 0):
                    if self.board[row][col] != '1':
                        if (row,col) is  (8,8) or (row,col) is  (1,1) or (row,col) is  (5,5) or (row,col) is  (4,4) :
                            return True

                else:
                    if self.board[row][col] != '0':
                        return False

        return True


        ##AI related ##

    def nullHeuristic(self):
        return 0


    """return move that I have - move that my opponent have"""
    def firstHeuristic(self,color):
        opcolor = None
        if color == '0':
            opcolor = '1'
        else:
            opcolor = '0'
        mymoves = self.get_possible_move_num(color)
        opmoves = self.get_possible_move_num(opcolor)
        if mymoves == 0:
            return -float("inf")
        if opmoves == 0:
            return float("inf")
        return mymoves-opmoves

def minimax(board, depth, alpha, beta, isMax, color, move):
    if depth == 0:
            return (board.firstHeuristic(color),(0,0,0,0))
    if isMax:
        value = -float("inf")
        actions = board.get_all_actions(color)
        bestaction = None
        for action in actions:
            print('yes')
            nextboard = board.get_next_board(action[0],action[1],action[2],action[3],color)
            curvalue = minimax(nextboard, depth - 1, alpha, beta, False, color,move)[0]
            curaction = minimax(nextboard, depth - 1, alpha, beta, False, color,move)[1]
            if curvalue > value:
                bestaction = action
            else:
                bestaction = curaction
            value = max(value, curvalue)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (value,bestaction)

    else:
        value = float("inf")

        actions = board.get_all_actions(color)
        for action in actions:
            nextboard = board.get_next_board(action[0], action[1], action[2], action[3], color)
            curvalue = minimax(nextboard, depth - 1, alpha, beta, True, color,move)[0]
            curaction = minimax(nextboard, depth - 1, alpha, beta, True, color,move)[1]
            if value > curaction:
                bestaction = action
            else:
                bestaction = curaction
            value = min(value, curvalue)
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (value, bestaction)

def start_game(width):
    board = Board(width)
    board.create_board(width)
    return board



board = start_game(8)
color = raw_input("pls choose black(1) or white(0)")
if color == '1':
    print("you choosed black, start the game now")
elif color == '0':
    print("you choosed white, start the game now")
    board.random_move('1')
    print("after black removed and move, the board:")
    board.print_board(board.board)
else: print("yo, wrong input")
if color == '0':
    oppocolor = '1'
else:
    oppocolor = '0'
while(1):
    moves = board.get_possible_move(color)
    if len(moves) == 0:
        print('you lost')
        break
    print('your possible moves are')
    print(moves)
    while(1):

        try:
            var = raw_input("pls enter the move num")
            var.split(" ")
            (fromx,fromy) = (int(var[0]),int(var[2]))
            (tox, toy) = (int(var[4]),int(var[6]))
            print(board.get_one_piece_movable(fromx,fromy))
            if board.get_one_piece_movable(fromx,fromy).count((tox,toy))==0:
                print("invalide move")
            else:
                board.next_board(fromx,fromy,tox,toy,color)
                print("heuristic return " + str(board.firstHeuristic(color)))

        except Exception:
            print("input error")

        print("minimax return " + str(minimax(board,3,float('inf'),-float('inf'),True,color,[])))

        board.print_board(board.board)
        break

    if board.random_move(oppocolor) is None:
        print("you win")
        break
    else:
        print("after black moved, the board:")
    board.print_board(board.board)
