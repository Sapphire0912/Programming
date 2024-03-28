from pprint import pprint

maze = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1]
]

directions = [
    lambda x, y: (x-1, y),
    lambda x, y: (x+1, y),
    lambda x, y: (x, y-1),
    lambda x, y: (x+1, y+1)
]


def maze_solve(x, y, goal_x, goal_y):
    maze[x][y] = 2
    stack = list()
    stack.append((x, y))
    print('迷宮開始')
    while len(stack) > 0:
        curr = stack[-1]  # 讀取最新路徑
        print('目前路徑: ', (curr[0], curr[1]))
        if curr[0] == goal_x and curr[1] == goal_y:
            print('抵達出口')
            return True

        for dire in directions:
            next_ = dire(curr[0], curr[1])
            if maze[next_[0]][next_[1]] == 0:
                stack.append(next_)
                maze[next_[0]][next_[1]] = 2  # 代表已走過
                break
        else:
            maze[curr[0]][curr[1]] = 3  # 死路
            stack.pop()
    else:
        print('沒有路徑')
        return False


maze_solve(1, 1, 4, 4)
pprint(maze)
