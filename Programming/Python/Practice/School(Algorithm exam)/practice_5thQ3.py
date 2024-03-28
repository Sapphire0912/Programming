def RR(A2, A1, m, n, LU, RU, LD, RD):
    ori_LU = [A1[0][0], A1[0][1], A1[1][0], A1[1][1]]
    ori_RU = [A1[0][n-2], A1[0][n-1], A1[1][n-2], A1[1][n-1]]
    ori_LD = [A1[m-2][0], A1[m-2][1], A1[m-1][0], A1[m-1][1]]
    ori_RD = [A1[m-2][n-2], A1[m-2][n-1], A1[m-1][n-2], A1[m-1][n-1]]

    # 右轉90度
    for k in range(4):
        LU[k] = ori_LD[k]
        RU[k] = ori_LU[k]
        LD[k] = ori_RD[k]
        RD[k] = ori_RU[k]


if __name__ == '__main__':
    m, n = list(map(int, input().rstrip().split()))
    A1 = list()

    for i in range(m):
        a = list(map(int, input().rstrip().split()))
        A1.append(a)

    A2 = list()
    LU = [0, 0, 0, 0]
    RU = [0, 0, 0, 0]
    LD = [0, 0, 0, 0]
    RD = [0, 0, 0, 0]
    RR(A2, A1, m, n, LU, RU, LD, RD)

    avgLU = 0
    avgRU = 0
    avgLD = 0
    avgRD = 0

    for i in range(4):
        avgLU = avgLU + LU[i]
        avgRU = avgRU + RU[i]
        avgLD = avgLD + LD[i]
        avgRD = avgRD + RD[i]

    no = 0.0000000001
    avgLU = round((avgLU + no) / 4)
    avgRU = round((avgRU + no) / 4)
    avgLD = round((avgLD + no) / 4)
    avgRD = round((avgRD + no) / 4)

    print(avgLU, avgRU, avgLD, avgRD)
