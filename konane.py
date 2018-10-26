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

    def print_board(self):
        for row in range(self.width + 1):
            for col in range(self.width + 1):
                print(self.board[row][col]),
            print

    def get_piece(self, x, y):
        if self.out_of_bound(x, y):
            # print("not valid coordinate")
            # raise Exception('coordinate not in range')
            pass
        else:
            return self.board[y][x]

    def get_one_piece_movable(self, x, y, flag = False):
        movable = []
        if self.out_of_bound(x, y) or self.get_piece(x,y) is ' ':
            print("not valid coordinate")
            raise Exception('coordinate not in range')
        if self.is_initial():
            #print('this is inital')
            if (x, y) == (8, 8) or (x, y) == (1, 1) or (x, y) ==(4, 4) or (x, y) == (5, 5):
                move = Move((x,y),(0,0))
                movable.append(move)
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
                move = Move((x,y),(0,0))
                movable.append(move)
            return movable

        else:
            newmove = []
            moves = []
            if flag:
                print(str(x)+' '+str(y)+' '+self.get_piece(x,y))
                print()
                #testing


            if self.check_movable(x,y,x+2,y,self.get_piece(x,y)):
                if flag:
                    print("L")
                moves.append(Move((x, y),(x+2,y),[(x+1,y)]))

            if self.check_movable(x,y,x-2,y,self.get_piece(x,y)):
                if flag:
                    print("R")
                moves.append(Move((x, y), (x - 2, y), [(x-1, y)]))

            if self.check_movable(x,y,x,y+2,self.get_piece(x,y)):
                if flag:
                    print("G")
                moves.append(Move((x, y), (x, y+2), [(x, y+1)]))

            if self.check_movable(x,y,x,y-2,self.get_piece(x,y)):
                if flag:
                    print("F")
                moves.append(Move((x, y), (x, y-2), [(x , y-1)]))

            for move in moves:
                newmove = self.recursive_move_helper(move, moves)

        return newmove

    def get_possible_move(self,color, flag = False):
        allmove = []
        for row in range(1,self.width + 1):
            for col in range(1,self.width + 1):

                if self.get_piece(row,col) == color:
                    moves = self.get_one_piece_movable(row, col, flag )
                    if len(moves)!=0:
                        allmove = allmove+moves
        return allmove
    '''generate the next board with the color, from coordinate and to coordinate'''
    def next_board(self,move,color):

        self.board_remove(move.fr[0], move.fr[1])

        for remove in move.removes:
            self.board_remove(remove[0], remove[1])

        if move.to[0] != 0:  # means not removing the piece (at the first second move you remove the piece)
            self.board_add(move.to[0], move.to[1], color)



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
        move = random.choice(moves)
        #move = moves[0]
        self.next_board(move,color)
        return move


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
            opcolor = '0'
        else:
            opcolor = '1'
        if x != tox:
            return self.get_piece((tox + x) / 2, toy) is opcolor and not self.out_of_bound(tox, y) and self.get_piece(tox, y) is ' '
        elif y != toy:
            return self.get_piece(x, (toy+y)/2) is opcolor and not self.out_of_bound(x, toy) and self.get_piece(x, toy) is ' '
        return True

    def get_possible_move_num(self,color):
        moves = self.get_possible_move(color)

        return len(moves)


    '''helper method to recursively find the mult step jump
    :parameter ox: original x of the piece  oy: original y of the piece, movable set of the piece, x,y is the coordinate we want to explore'''
    def recursive_move_helper(self, move,moves):
        x = move.to[0]
        y = move.to[1]
        ox = move.fr[0]
        oy = move.fr[1]
        removes = move.removes
        if self.check_movable(x, y, x + 2, y,self.get_piece(ox,oy)):
            if removes.count((x+1,y))==0:
                newmove = Move((ox, oy), (x + 2, y), removes + [(x + 1, y),])
                if moves.count(newmove)==0:
                    moves.append(newmove)
                    self.recursive_move_helper(newmove,moves)

        if self.check_movable(x, y, x - 2, y, self.get_piece(ox,oy)):
            if removes.count((x-1,y))==0:
                newmove = Move((ox, oy), (x - 2, y), removes + [(x - 1, y),])
                if moves.count(newmove) == 0:
                    moves.append(newmove)
                    self.recursive_move_helper(newmove,moves)

        if self.check_movable(x, y, x, y + 2, self.get_piece(ox,oy)):
            if removes.count((x,y+1))==0:
                newmove = Move((ox, oy), (x , y +2), removes + [(x, y+1),])
                if moves.count(newmove) == 0:
                    moves.append(newmove)
                    self.recursive_move_helper(newmove,moves)

        if self.check_movable(x, y, x, y - 2, self.get_piece(ox,oy)):
            if removes.count((x,y -1))==0:
                newmove = Move((ox, oy), (x , y -2), removes + [(x, y-1),])
                if moves.count(newmove) == 0:
                    moves.append(newmove)
                    self.recursive_move_helper(newmove,moves)
        cleanlist = []
        [cleanlist.append(x) for x in moves if x not in cleanlist]
        return cleanlist

    def get_next_board(self,move,color):
        import copy
        c = copy.deepcopy(self)
        c.board_remove(move.fr[0], move.fr[1])
        for remove in move.removes:
            c.board_remove(remove[0],remove[1])

        if move.to[0]!=0: #means not removing the piece (at the first move you remove the piece)

            c.board_add(move.to[0],move.to[1],color)

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



                elif sum(x.count(' ') for x in self.board)==2 and (row + col) % 2 == 0:
                    if self.board[row][col] == ' ':
                        if (row,col) ==  (8,8) or (row,col) ==  (1,1) or (row,col) ==  (5,5) or (row,col) ==  (4,4) :
                            return True

                else:
                    if self.board[row][col] != '0':
                        return False

        return False

        def change_board(board):
            self.board = board

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

    def print_move(self,moves):
        index = 0
        for move in moves:
            index += 1
            print(str(index)+": "+str(move))

def minimax(board, depth, alpha, beta, isMax, color, move):
    if depth == 0:
            return (board.firstHeuristic(color),(0,0,0,0))
    if isMax:
        value = -float("inf")
        moves = board.get_possible_move(color)
        bestaction = None
        for move in moves:
            nextboard = board.get_next_board(move,color)
            curvalue = minimax(nextboard, depth - 1, alpha, beta, False, color,move)[0]
            curaction = minimax(nextboard, depth - 1, alpha, beta, False, color,move)[1]
            if curvalue > value:
                bestaction = move
            else:
                bestaction = curaction
            value = max(value, curvalue)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (value,bestaction)

    else:
        value = float("inf")

        actions = board.get_possible_move(color)
        for action in actions:
            nextboard = board.get_next_board(move, color)
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


class Move:
    def __init__(self,fr, to, removes = []):
        self.fr = fr
        self.to = to
        self.removes =removes

    def __str__(self):
        return 'from '+str(self.fr)+ 'to '+str(self.to)+' this removes '+str(self.removes)

    def __eq__(self, other):
        return self.fr == other.fr and self.to == other.to and set(self.removes) == set(other.removes)

    def __ne__(self, other):
        return not self.__eq__(other)


def start_game(width):
    board = Board(width)
    board.create_board(width)
    return board



board = start_game(8)


'''board.board = [[' ', 1, 2, 3, 4, 5, 6, 7, 8], [1, '1', '0', ' ', ' ', '1', '0', '1', '0'], [2, ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'], [3, ' ', '0', ' ', ' ', ' ', '0', '1', ' '], [4, ' ', ' ', ' ', '1', ' ', '1', ' ', ' '], [5, ' ', '0', ' ', ' ', '1', ' ', '1', ' '], [6, '0', ' ', '0', ' ', '0', ' ', '0', ' '], [7, '1', ' ', ' ', ' ', ' ', '0', '1', ' '], [8, '0', '1', ' ', '1', '0', '1', ' ', '1']]

board.print_board()
board.print_move(board.get_possible_move('0'))
board.print_move(board.get_possible_move('1'))'''



color = raw_input("pls choose black(1) or white(0)")
if color == '1':
    print("you choosed black, start the game now")
elif color == '0':
    print("you choosed white, start the game now")
    board.random_move('1')
    print("after black removed and move, the board:")
    board.print_board()
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
    board.print_move(moves)
    while(1):
        while(1):
            try:
                #var = raw_input("pls enter the move num")
                #index = int(var)
                index = 1
                if index>len(moves):
                    print("invalide move")
                    continue
                else:
                    board.next_board(moves[index-1],color)
                    print("heuristic return " + str(board.firstHeuristic(color)))


            except Exception:
                print("input error")
            else:
                break


        #print("minimax return " + str(minimax(board,3,float('inf'),-float('inf'),True,color,[])))

        board.print_board()
        info = board.board
        board = start_game(8)
        board.print_board()
        board.board=info

        break

    if len( board.get_possible_move(oppocolor)) == 0:
        print("you win")
        break
    else:

        print('opponent move: ')
        print(str(board.random_move(oppocolor)))

        print("after black moved, the board:")



board.print_move(board.get_possible_move('1'))
print(board.board)

c = start_game(8)
c.board = board.board
print('for c')
c.print_board()
c.print_move(c.get_possible_move('1'))
