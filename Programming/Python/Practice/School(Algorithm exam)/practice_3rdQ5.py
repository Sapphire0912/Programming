def circular_queue(c, y):
    global rear, x, front

    if c == 'i':
        queue[rear] = y
        rear += 1
        visited[y] = 1

    if c == 'd':
        front += 1
        x = queue[front]
    # ????

def bfs(src, p):
    global rear, front, x
    print(p)
    visited[p] = 1

    for i in range(10):
        if src[p][i] == 1:
            if visited[i] != 1:
                circular_queue('i', i)
    print(queue)
    print(rear, front, x)

    while front != rear:
        circular_queue('d', x)
        if visited[x] != 1:
            bfs(src, x)


if __name__ == '__main__':
    N = 10
    rear, front, x = 0, 0, 0
    queue = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    visited = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    src = [[0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
           [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
           [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
           [1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
           [0, 1, 0, 1, 0, 1, 1, 0, 0, 0],
           [0, 0, 0, 1, 1, 0, 1, 1, 0, 0],
           [0, 0, 0, 0, 1, 1, 0, 1, 1, 0],
           [0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
           [0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
           [0, 0, 0, 0, 0, 0, 0, 1, 1, 0]]

    p = int(input())
    bfs(src, p)
