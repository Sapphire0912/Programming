# Fibonacci
def fib(i):
    if i in [0, 1]:
        return i
    else:
        return fib(i - 1) + fib(i - 2)


# print(fib(9))

# tower of hanoi
def hanoi(n, src, aux, dst):
    """
    n: 有 n 個數目的圓盤
    src: 柱子 A, 圓盤一開始在的位置
    aux: 柱子 B, 一開始是空的, 用來輔助移動的柱子
    dst: 柱子 C, 圓盤最後要移動到的目的地

    解法:
    1. 將 n - 1 個盤子, 從 柱子 A 移動到 柱子 B
    2. 將 n 個盤子, 從 柱子 A 移動到 柱子 C
    3. 將 n - 1 個盤子, 從 柱子 B 移動到 柱子 C
    (第一次移動盤子時: n 是偶數時, A -> B; n 是奇數時, A -> C)
    """
    global step  # 儲存移動次數

    if not n:
        return 0

    if n == 1:
        # n = 1, 奇數會把圓盤從 柱子 A -> 柱子 C; src -> dst
        step += 1
        print('{0:2d}: 移動圓盤 {1}, 從 {2} 到 {3}'.format(step, n, src, dst))

    else:
        # n 是偶數時, 會把圓盤從 柱子 A -> 柱子 B; src -> aux; 解法 1
        hanoi(n - 1, src, dst, aux)  # 此時柱子 C 會是輔助柱子, dst 參數會在 aux 的位置

        step += 1
        print('{0:2d}: 移動圓盤 {1}, 從 {2} 到 {3}'.format(step, n, src, dst))

        # n 是偶數時, 會把圓盤從 柱子 B -> 柱子 C; aux -> dst ; 解法 3
        hanoi(n - 1, aux, src, dst)


step = 0
# n = int(input("圓盤數量:"))
# hanoi(n, 'A', 'B', 'C')


# 8-Queen
def check(row, col):
    for k in range(1, row + 1):
        pos = queens[row - k]
        if pos in [col, col + k, col - k]:
            return False
    return True


def location(row):
    """尋找特定 row 的 col 欄位"""
    start = queens[row] + 1
    for col in range(start, SIZE):
        if check(row, col):
            return col
    return -1


def solve():
    """從特定 row 開始尋找 Queen 位置"""
    row = 0
    while 0 <= row <= 7:
        col = location(row)
        if col < 0:
            queens[row] = -1
            row -= 1
        else:
            queens[row] = col
            row += 1

    return row != -1


SIZE = 8
queens = [-1] * SIZE
# solve()
# print('queens: ', queens)
#
# for i in range(SIZE):
#     for j in range(SIZE):
#         if queens[i] == j:
#             print('Q', end='')
#         else:
#             print('1', end='')
#     print()


# 8-Queen(class, recursive)
class Queens(object):
    def __init__(self):
        self.queens = [-1] * size
        self.solve(0)

        for i in range(size):
            for j in range(size):
                if self.queens[i] == j:
                    print('Q', end='')
                else:
                    print('1', end='')
            print()

    def is_OK(self, row, col):
        for k in range(1, row + 1):
            pos = self.queens[row - k]
            if pos in [col, col + k, col - k]:
                return False
        return True

    def solve(self, row):
        if row == size:
            return True

        for col in range(size):
            self.queens[row] = col
            if self.is_OK(row, col) and self.solve(row + 1):
                return True
        return False


size = 8
# Queens()


# Fractal
from tkinter import *


def drawLine(p1, p2):
    canvas.create_line(p1[0], p1[1], p2[0], p2[1], tags='H-tree')


def show():
    canvas.delete("H-tree")
    length = 200
    center = [200, 200]
    H_tree(order.get(), center, length)


def H_tree(order, center, ht):
    """
    依指定階級數繪製 H-Tree 碎形
    """

    if order >= 0:
        p1 = [center[0] - ht / 2, center[1] - ht / 2]
        p2 = [center[0] - ht / 2, center[1] + ht / 2]
        p3 = [center[0] + ht / 2, center[1] - ht / 2]
        p4 = [center[0] + ht / 2, center[1] + ht / 2]

        drawLine([center[0] - ht / 2, center[1]], [center[0] + ht / 2, center[1]])
        drawLine(p1, p2)
        drawLine(p3, p4)

        H_tree(order - 1, p1, ht / 2)
        H_tree(order - 1, p2, ht / 2)
        H_tree(order - 1, p3, ht / 2)
        H_tree(order - 1, p4, ht / 2)


tk = Tk()
canvas = Canvas(tk, width=400, height=400)
canvas.pack()

frame = Frame(tk)
frame.pack(padx=5, pady=5)

Label(frame, text="輸入 H-Tree 階數: ").pack(side=LEFT)
order = IntVar()
order.set(0)

entry = Entry(frame, textvariable=order).pack(side=LEFT, padx=3)
Button(frame, text="顯示 H-Tree", command=show).pack(side=LEFT)
tk.mainloop()




