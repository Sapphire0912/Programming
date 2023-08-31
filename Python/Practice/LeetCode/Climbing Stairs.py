# You are climbing a staircase. It takes n steps to reach the top.
# Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

def climbStairs(n):
    """
    solve: x + 2y = n, (x, y >= 0)
    x = n - 2y (iteration)
    C (x + y) 取 y
    """

    ans = 0
    combines = 1

    # 計算所有可行解
    list_xy = list()
    for y in range(0, n+1):
        x = n - 2 * y

        if isinstance(x, int) and x >= 0:
            list_xy.append((x, y))

    # 可行解都是一個排列組合
    for index in list_xy:
        # (x + y)!
        for t in range(1, sum(index) + 1):
            combines *= t

        # x!
        for xx in range(1, min(index) + 1):
            combines //= xx

        # y!
        for yy in range(1, max(index) + 1):
            combines //= yy

        ans += combines
        combines = 1
    return int(ans)


print(climbStairs(41))
