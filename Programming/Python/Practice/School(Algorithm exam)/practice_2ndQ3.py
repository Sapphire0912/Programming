def fee(S, D):
    start, end = name.index(S), name.index(D)
    if start > end:
        start, end = end, start
    return sum(price[start:end])


if __name__ == "__main__":
    station = list(map(str, input().rstrip().split()))
    card = str(input())

    name = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]
    price = [12, 15, 8, 10, 13, 8, 10, 12, 16, 0]

    S, D = station[0], station[1]
    money = fee(S, D)

    if card == 'Y' or card == 'y':
        money = round(money * 0.8)
    print(money)
