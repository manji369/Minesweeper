import random, re, time, sys
from string import ascii_lowercase

class Minesweeper:

    def __init__(self, gridSize, probX, allowedChars):
        self.gridSize = gridSize
        self.grid = [[False]*self.gridSize[1] for i in range(self.gridSize[0])]
        self.posDict = {'X': set()}
        self.visited = set()
        self.probX = probX
        self.allowedChars = allowedChars

    def _isValid(self, pos):
        return pos[0] >= 0 and pos[0] < self.gridSize[0] and pos[1] >= 0 and pos[1] < self.gridSize[1]

    def _updateNumbers(self):
        for pos in self.posDict['X']:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    newPos = pos[0]+i, pos[1]+j
                    if self._isValid(newPos) and self.grid[newPos[0]][newPos[1]][0] != 'X':
                        self.grid[newPos[0]][newPos[1]] = (str(int(self.grid[newPos[0]][newPos[1]][0]) + 1), False, False)

    def _initializeGrid(self):
        for i in range(self.gridSize[0]):
            for j in range(self.gridSize[1]):
                ch = self.allowedChars[1]
                if random.uniform(0, 1) < self.probX:
                    ch = self.allowedChars[0]
                self.grid[i][j] = (ch, False, False)
                if ch == 'X':
                    self.posDict['X'].add((i,j))
        self._updateNumbers()

    def _cellValue(self, cellTuple, override=False):
        if override:
            return cellTuple[0]
        if cellTuple[1]:
            return 'f' if cellTuple[2] else cellTuple[0]
        return ' '

    def _showGrid(self, override=False):
        print('  ' + '   '.join(ascii_lowercase[:self.gridSize[1]]))
        print()
        print(' ' + '--- '*self.gridSize[1])
        for i, row in enumerate(self.grid):
            print('| ' + ' | '.join([self._cellValue(val, override) for val in row]), end=' |')
            print('  ' + str(i+1), end='\n')
            print(' ' + '--- '*self.gridSize[1])

    def _parseInput(self):
        inp = input()
        if inp == 'stop':
            return []
        splitInp = inp.split(' ')
        flag = ' no flag'
        if len(splitInp) == 2:
            col, row = splitInp
        elif len(splitInp) == 3:
            col, row, flag = splitInp
            if flag.lower() != 'f':
                print("Flag variable (f or F) is to be sent as third argument")
                print("Please try again")
                return self._parseInput()
        else:
            print("Number of inputs exceeded or not reached. Min: 2, Max: 3, got: " + str(len(splitInp)))
            print("Please try again")
            return self._parseInput()
        print("You entered: {0}{1}{2}".format(col, row, flag))
        try:
            res = int(row)-0 > self.gridSize[0] or ord(col)-ord('a')+1 > self.gridSize[1]
        except:
            print("Given input is not in required format")
            print("Please try again")
            return self._parseInput()
        if res:
            print("Given input is out of bounds.")
            print("Please try again")
            return self._parseInput()
        return [ord(col)-ord('a'), int(row)-1, flag=='f']

    def _expandSelection(self, i, j):
        if not self._isValid((i, j)) or (i, j) in self.visited:
            return
        ch = self.grid[i][j][0]
        if ch == 'X':
            pass
        elif ch == '0':
            for row in range(-1, 2):
                for col in range(-1, 2):
                    newI, newJ = i+row, j+col
                    if row == 0 and col == 0:
                        self.grid[newI][newJ] = self.grid[newI][newJ][0], True, self.grid[newI][newJ][2]
                        self.visited.add((newI, newJ))
                    self._expandSelection(newI, newJ)
        else:
            self.grid[i][j] = self.grid[i][j][0], True, self.grid[i][j][2]
            self.visited.add((i, j))

    def _updateGrid(self, inp, lost=False):
        if not lost:
            col, row, flag = inp
            if self.grid[row][col][0] == 'X' and not flag:
                return 'lost'
            else:
                if flag:
                    self.grid[row][col] = (self.grid[row][col][0], not self.grid[row][col][1], not self.grid[row][col][2])
                else:
                    self._expandSelection(row, col)
                    if len(self.visited) + len(self.posDict['X']-self.visited) >= self.gridSize[0]*self.gridSize[1]:
                        return 'win'
        else:
            for i in range(self.gridSize[0]):
                for j in range(self.gridSize[1]):
                    self.grid[i][j] = (self.grid[i][j][0], True, False)


    def startGame(self):
        self._initializeGrid()
        self._showGrid()
        print('\nEnter "stop" to stop the game any time\n')
        print('Enter the column alphabet, row number and optional flag (f) separated b space.\n')
        print('eg1. "a 3 f" will mark a,3 with flag.\n')
        print('eg2. "a 3" will click on a3.\n')
        inp = True
        while inp:
            inp = self._parseInput()
            if inp:
                result = self._updateGrid(inp)
                if result == 'win':
                    self._showGrid(override=True)
                    print("\nCongratulations! You won!\n")
                    print("Want to play again? (y/n)")
                    promtInp = input()
                    if promtInp.lower() == 'y':
                        return self.startGame()
                    else:
                        break
                elif result == 'lost':
                    print("You Lost :(")
                    self._updateGrid(inp, lost=True)
                    self._showGrid()
                    print("Want to play again? (y/n)")
                    promtInp = input()
                    if promtInp.lower() == 'y':
                        return self.startGame()
                    else:
                        break
                self._showGrid()

def updateGridSize(args):
    gridSize = (9, 9)
    probX = 0.1
    try:
        assert len(args) == 2 or len(args) == 3
        x, y = int(args[0]), int(args[1])
        if len(args) == 3:
            probX = float(args[2])
        assert x > 0 and y > 0 and x < 21 and y < 21
        gridSize = x, y
    except:
        print("\nPlease specify grid size with two numbers separated by space.")
        print("Eg. 9 9")
        print("Assuming grid size to be: 9x9\n")
    finally:
        return (gridSize, probX)

if __name__ == '__main__':
    allowedChars = ['X', '0']
    gridSize, probX = updateGridSize(sys.argv[1:])
    minesweeperObj = Minesweeper(gridSize, probX, allowedChars)
    minesweeperObj.startGame()
