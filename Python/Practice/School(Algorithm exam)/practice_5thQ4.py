def match(bet, record):
    special = record[-1]
    score = 0
    for k in bet:
        if k in record[:len(record) - 1]:
            score += 1

    isSpecial = 1 if special in bet else 0
    res = [score, isSpecial]
    tar = [[5, 1], [5, 0], [4, 1], [4, 0], [3, 1], [3, 0], [2, 1]]

    if score == 6:
        return 1
    elif res in tar:
        index = tar.index(res)
        return index + 2
    else:
        return 0


if __name__ == '__main__':
    bet = input().split()
    num = int(input())
    prize = [0] * 9

    for i in range(num):
        record = input().split()
        prize[match(bet, record)] += 1
    print(*prize[1:])
