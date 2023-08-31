def MusicOrder(chapter_len, X_sorted, X_sorted_id):
    result = list()
    k = 0
    t = chapter_len
    while k != len(X_sorted_id):
        tick, num = X_sorted[k], X_sorted_id[k]

        if t >= tick:
            t -= tick
            X_sorted.remove(tick)
            X_sorted_id.remove(num)
            result.append(num + 1)
        else:
            k += 1

    return result


if __name__ == "__main__":
    M = int(input())
    X = [None]
    X_sorted = [None] * M  # 排序後的音樂歌單時長
    X_sorted_id = [None] * M  # 排序後的音樂清單編號

    X_all = input() # 輸入音樂歌單時長
    X = X_all.split(' ')
    X = list(map(int, X))

    X_sorted[0] = X[0]
    X_sorted_id[0] = 0
    for i in range(1, M):
        key = X[i]
        j = i - 1
        while(j>=0 and X_sorted[j]<=key):
            X_sorted[j+1] = X_sorted[j]
            X_sorted_id[j+1] = X_sorted_id[j]
            j -= 1
        X_sorted[j+1] = key
        X_sorted_id[j+1] = i

    # 安排四個單元的歌單
    chapter_len = 13 * 60 # 每個單元時長
    rounds = 4 # 單元數量

    for r in range(rounds):
        music_list = MusicOrder(chapter_len, X_sorted, X_sorted_id)
        music_list_len = len(music_list)
        remain = chapter_len
        for m in music_list:
            remain -= X[m-1]
            print(m, end=" ")  # 印出該單元的音樂播放清單
        print(remain)  # 印出該單元剩餘時間
