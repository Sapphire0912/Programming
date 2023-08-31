def selectCourse(candidates, selected):
    times = [1, 2, 3, 4, 5, 6, 7, 8]
    lesson, start_time, end_time, res = list(), list(), list(), list()

    # 將 Data 拆開, 找出 index 為選中當前課號
    for info in candidates:
        lesson.append(info[1])
        start_time.append(info[2])
        end_time.append(info[3])

    while len(lesson) > 0:
        # 2. 挑選最早下課者
        earliest = min(end_time)

        # 判斷是否有同時間結束的
        target = list()
        for k, t in enumerate(end_time):
            if t == earliest:
                target.append(k)

        if len(target) > 1:
            # 代表有同時間結束的課程 (按照英文字母排序較前者)
            index = lesson.index(min(lesson))
        else:
            index = target[0]

        # 4. 判斷課程時間不可重疊
        key = 1
        for k in range(start_time[index], end_time[index]+1):
            if k not in times:
                key = 0
                break

        if key:
            # 5. 相同課程在三天內只能選一次
            if lesson[index] not in selected:
                for k in range(start_time[index], end_time[index]+1):
                    times.remove(k)
                # 將課選上, 加入 res list 裡面
                res.append([candidates[0][0], lesson[index], start_time[index], end_time[index]])

        # 移除已選的課程
        lesson.pop(index)
        start_time.pop(index)
        end_time.pop(index)

    return res


if __name__ == '__main__':
    n = int(input())
    allcourse = list()
    candidates = list()
    selected = list()

    for i in range(n):
        courses = input()
        dataSplit = courses.split(' ')
        allcourse.append([int(dataSplit[0]), dataSplit[1], int(dataSplit[2]), int(dataSplit[3])])

    for i in range(3):
        for j in range(n):
            if allcourse[j][0] == i + 1:
                candidates.append(allcourse[j])

        result = selectCourse(candidates, selected)
        candidates = list()

        for x in result:
            selected.append(x[1])
            for z in x:
                print(str(z), end=" ")
            print("")