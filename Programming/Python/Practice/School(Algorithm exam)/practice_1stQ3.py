def WinPrize(W, P):
    prize = [0, 0, 0, 200, 1000, 4000, 10000, 40000, 200000]
    count = 0
    for k in range(7, -1, -1):
        if W[k] == P[k]:
            count += 1
        else:
            break
    return prize[count]


if __name__ == '__main__':
    W = input()
    N = int(input())
    M = 0

    for i in range(N):
        P = input()
        M += WinPrize(W, P)
    print(M)

