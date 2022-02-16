import sys
from itertools import chain
import time

sys.setrecursionlimit(1000)

tab = []

imp = open("sudoku.txt").read().split()

for i in range(9):
    tab.append(list(map(int, imp[(i*9):(9+i*9)])))


def possi(y, x, n):
    for i in range(9):
        if (tab[i][x] == n) or (tab[y][i] == n):
            return False
    x3 = (x // 3) * 3
    y3 = (y // 3) * 3
    for i in range(3):
        for j in range(3):
            if tab[j + y3][i + x3] == n:
                return False
    return True


def solve(tab):
    test = sum(tab, [])
    if 0 in test:

        for y in range(9):

            for x in range(9):

                if tab[y][x] == 0:

                    for n in range(1, 10):

                        if possi(y, x, n):

                            tab[y][x] = n

                            solve(tab)

                        if n == 9:
                            tab[y][x] = 0
                            return False

        return True
    else:
        for i in tab:
            print(i)
        return True


for i in tab:
    print(i)

print()
time1 = time.time()
solve(tab)
time2 = time.time()
print(1000*(time2 - time1), "ms")

