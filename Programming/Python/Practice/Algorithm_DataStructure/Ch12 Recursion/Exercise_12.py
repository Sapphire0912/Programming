# 3.
def f(n, count):
    if n == 0:
        return count
    return f(n - 1, count + 1 / n)


# print(f(5, 0))


# 4.
def f2(n, count):
    if n == 0:
        return count
    return f2(n - 1, count + n / (n + 1))


# print(f2(5, 0))


# 5.
def hanoi(n, src, aux, dst):
    global step
    if not n:
        return 0

    if n == 1:
        step += 1
        print('{0:2d}: 移動圓盤 {1} 從 {2} 到 {3}'.format(step, n, src, dst))

    else:
        hanoi(n - 1, src, dst, aux)
        step += 1
        print('{0:2d}: 移動圓盤 {1} 從 {2} 到 {3}'.format(step, n, src, dst))
        hanoi(n - 1, aux, src, dst)


step = 0
hanoi(4, 'A', 'C', 'B')
