def WhoOut(clockwise, count_m):
    global count
    curr_student = len(student)
    print("curr_std: ", student, "count: ", count)
    count_m %= curr_student
    count_m -= 1

    if clockwise == 'R':
        count += count_m
        while count > curr_student:
            count -= curr_student
        std = student[count]
        student.remove(std)

    elif clockwise == 'B':
        count -= count_m
        while count < (-curr_student):
            count += curr_student
        std = student[count]
        student.remove(std)

    return std


if __name__ == '__main__':
    poker = [i for i in range(0, 52)]
    color = ["黑桃", "紅心", "方塊", "梅花"]

    N = int(input())  # 學生人數
    M = int(input())

    if M > N:
        print("error occur")
    else:
        student = [i for i in range(1, N+1)]
        count = 0  # 第幾位學生,初始接從第一位開始數
        poker = []

        for i in range(M):
            p = input()
            R, B = p[0], int(p[1:])
            poker.append([R, B])

        for i in range(M):
            print(WhoOut(poker[i][0], poker[i][1]))
