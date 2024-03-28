def BugFinder(x, y):
    history = [[x, y]]
    lookup = [[x, y]]

    if maps[x][y] == 1:
        a = 1
    else:
        return 0

    def up(cx, cy):
        if cx == 1:
            return False
        else:
            new_x, new_y = cx - 1, cy
            if [new_x, new_y] in history:
                return False
            elif maps[new_x][new_y] == 0:
                return False
            else:
                history.append([new_x, new_y])
                lookup.append([new_x, new_y])
                return True

    def down(cx, cy):
        if cx == M:
            return False
        else:
            new_x, new_y = cx + 1, cy
            if [new_x, new_y] in history:
                return False
            elif maps[new_x][new_y] == 0:
                return False
            else:
                history.append([new_x, new_y])
                lookup.append([new_x, new_y])
                return True

    def left(cx, cy):
        if cy == 1:
            return False
        else:
            new_x, new_y = cx, cy - 1
            if [new_x, new_y] in history:
                return False
            elif maps[new_x][new_y] == 0:
                return False
            else:
                history.append([new_x, new_y])
                lookup.append([new_x, new_y])
                return True

    def right(cx, cy):
        if cy == N:
            return False
        else:
            new_x, new_y = cx, cy + 1
            if [new_x, new_y] in history:
                return False
            elif maps[new_x][new_y] == 0:
                return False
            else:
                history.append([new_x, new_y])
                lookup.append([new_x, new_y])
                return True

    while len(lookup) > 0:
        now_x, now_y = lookup[-1]
        if up(now_x, now_y) or down(now_x, now_y) or left(now_x, now_y) or right(now_x, now_y):
            a += 1
            continue
        lookup.pop()

    return a


maps = []
visit = []
# dfs

if __name__ == '__main__':
    M, N = input().split()
    M = int(M)
    N = int(N)

    maps = [[0 for _ in range(N+2)]]

    for i in range(1, M+1):
        maps.append(input().split())
        maps[i] = list(map(int, maps[i]))
        maps[i] = [0] + maps[i] + [0]

    maps.append([0 for _ in range(N+2)])

    x, y = input().split()
    x, y = int(x), int(y)

    area = BugFinder(x+1, y+1)
    print(area)
    print(maps)
