def ContainerOrder(maps, container_no):
    tx, ty = 0, 0
    for y in range(7):
        for x in range(10):
            if maps[y][x] == container_no:
                tx, ty = x, 6 - y
                break

    # 判斷要從左上拿還是右上拿
    disL = ((6 - ty) ** 2 + tx ** 2) ** 0.5
    disR = ((6 - ty) ** 2 + (9 - tx) ** 2) ** 0.5

    take = list()
    if disL < disR:
        for y in range(7 - ty):
            for x in range(tx + 1):
                if maps[y][x] == container_no:
                    break
                take.append(maps[y][x])
    else:
        for y in range(7 - ty):
            for x in range(9, tx - 1, -1):
                if maps[y][x] == container_no:
                    break
                take.append(maps[y][x])

    return take


if __name__ == '__main__':
    container_no = int(input())

    maps = [[1, 40, 65, 22, 35, 55, 14, 53, 64, 42],
            [17, 28, 44, 10, 43, 3, 27, 34, 54, 19],
            [41, 18, 62, 45, 39, 21, 8, 70, 13, 63],
            [31, 49, 5, 25, 61, 36, 2, 56, 59, 4],
            [23, 58, 11, 15, 9, 52, 67, 24, 46, 26],
            [7, 48, 30, 57, 32, 29, 16, 51, 69, 38],
            [33, 66, 6, 37, 60, 47, 12, 68, 20, 50]]  # 貨櫃排列地圖

    container_list = ContainerOrder(maps, container_no)
    print(len(container_list)*3)

    for e in container_list:
        print(e, end=" ")
    print()
