def SeatChecked(R, C, VIPSeats, Seat):
    px, py = Seat

    for coord in VIPSeats:
        x, y = coord
        dis = ((px - x) ** 2 + (py - y) ** 2) ** 0.5

        if dis <= 1:
            return 0
    return 1


if __name__ == "__main__":
    VIPSeats = list()
    R = int(input())
    C = int(input())
    n = int(input())

    for k in range(n):
        try:
            VIPSeats.append(list(map(int, input().rstrip().split())))
        except EOFError:
            break

    num = 0
    for i in range(R):
        for j in range(C):
            check = [i, j]
            check = SeatChecked(R, C, VIPSeats, check)
            if check == 1:
                num += 1
    print(num)
