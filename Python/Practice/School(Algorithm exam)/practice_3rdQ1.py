def Ball(S):
    board, Score = S[:7], S[7:]

    if board[0]:  # 1 -> 彈向右邊
        # 判斷 3, 6, 7
        S[0] = 0
        if board[2]:  # 3 -> 彈向右邊
            # 判斷 7
            S[2] = 0
            if board[6]:
                S[6] = 0
                return Score[7]
            else:
                S[6] = 1
                return Score[6]
        else:  # 3 -> 彈向左邊
            # 判斷 6
            S[2] = 1
            if board[5]:
                S[5] = 0
                return Score[5]
            else:
                S[5] = 1
                return Score[4]
    else:
        # 判斷 2, 4, 5
        S[0] = 1
        if board[1]:  # 2 -> 彈向右邊
            # 判斷 5
            S[1] = 0
            if board[4]:
                S[4] = 0
                return Score[3]
            else:
                S[4] = 1
                return Score[2]
        else:  # 2 -> 彈向左邊
            # 判斷 4
            S[1] = 1
            if board[3]:
                S[3] = 0
                return Score[1]
            else:
                S[3] = 1
                return Score[0]


if __name__ == '__main__':
    N = int(input())
    S = [int(e) for e in input().split()]
    S += [1, 2, 3, 1, 1, 2, 3, 1]
    score = 0

    for i in range(N):
        score += Ball(S)
    print(score)
