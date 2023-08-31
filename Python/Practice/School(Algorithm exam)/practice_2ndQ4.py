def selectCourse(candidates, selected):
    times = [1, 2, 3, 4, 5, 6, 7, 8]
    res = list()
    s = dict()
    t = dict()

    for info in candidates:
        if info[3] not in s.keys():
            s[info[3]] = list()  # end: [lesson]
            t[info[1]] = [info[2], info[3]]  # lesson: [start, end]
        s[info[3]].append(info[1])

    while len(s.keys()) > 0:
        min_end = min(s.keys())
        target = s[min_end]

        if len(target) > 1:
            target.sort()
        lesson = target[0]

        if lesson not in selected:
            start, end = t[lesson]
            key = 1
            for k in range(start, end+1):
                if k not in times:
                    key = 0
                    break

            if key:
                for k in range(start, end+1):
                    times.remove(k)
                res.append([candidates[0][0], lesson, start, end])

        s[min_end].remove(lesson)
        if len(s[min_end]) == 0:
            s.pop(min_end)

    return res

# 測驗平台無法編譯


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
