def WaveCount(prices, start, R):
    low, high = prices[start], 0
    bound = low * R

    return -1


if __name__ == '__main__':
    R = float(input())  # 漲幅比率值
    N = int(input())  # 股價資料數量
    dates = []  # 股價資料的日期
    prices = []  # 股價資料的收盤價

    for i in range(N):
        stock = input()
        d, p = stock.split()
        dates.append(d)
        prices.append(float(p))

    start = 0
    wave_num = 0

    while start < N-2:
        end = WaveCount(prices, start, R)

        if end != -1:
            real_rate = round((prices[end]/prices[start] - 1.0) * 100.0, 1)
            print(dates[start], round(prices[start], 1), dates[end], round(prices[end], 1), str(real_rate) + '%', end = "\n")
            start = end + 1
            wave_num += 1

    percent = R * 100
    if wave_num > 0:
        print("本支股票從 " + dates[0] + " 到 " + str(dates[N - 1]) + " 間超過" + str(percent) + "%漲幅共" +
              str(wave_num) + "次", end="\n")
    else:
        print("本支股票從 " + dates[0] + " 到 " + str(dates[N-1]) + " 無所設定" + str(percent) + "%之漲幅", end="\n")
