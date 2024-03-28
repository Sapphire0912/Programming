def ConnectedComponent(x, y, grid):
    pass


if __name__ == '__main__':
    origrid = []
    grid = []

    for k in range(1):
        try:
            x, y = map(int, input().split())
        except EOFError:
            break

    m = int(input())
    n = int(input())

    for k in range(m):
        try:
            grid.append(list(map(int, input().rstrip().split())))
        except EOFError:
            break

    for q in range(m):
        s = []
        for r in range(n):
            s.append(grid[q][r])
        origrid.append(s)

    allxy = []
    mark = 10
    for i in range(m):
        for j in range(n):
            check = [i, j]
            grid, xy = ConnectedComponent(i, j, grid)
            for k in range(m):
                for l in range(n):
                    if grid[k][l] == 2:
                        grid[k][l] = mark

            if xy != []:
                allxy.append(xy)
            mark += 1

    yes = 0
    tian = 0
    if grid[x][y] == 0:
        print("None")
    else:
        for i in range(len(allxy)):
            if x >= allxy[i][0] and y >= allxy[i][1] and x <= allxy[i][2] and y <= allxy[i][3]:
                for iii in range(allxy[i][2]-allxy[i][0]+1):
                    for jjj in range(allxy[i][3]-allxy[i][1]+1):
                        if grid[allxy[i][0]+iii][allxy[i][1]+jjj] == 0:
                            tian = tian + 1
                        elif grid[allxy[i][0]+iii][allxy[i][1]+jjj] != grid[x][y]:
                            yes = 1

        if yes == 1:
            print("Overlapped")
        else:
            print(tian)