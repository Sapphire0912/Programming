def average(data, n):
    avg = 0
    for x in data:
        avg += x

    return avg // n


def split(data, left, right):
    pivot = data[left]
    pivot_position = left

    for i in range(left+1, right+1):
        if data[i] < pivot:
            pivot_position += 1
            data[i], data[pivot_position] = data[pivot_position], data[i]
        print('i =', i, "Data:", data, "left, right =", left, right)

    data[left], data[pivot_position] = data[pivot_position], data[left]
    print("last Data:", data)

    return pivot_position


def split_range(pivot_position, mid, left, right):
    if pivot_position < mid:
        left = pivot_position + 1

    if pivot_position > mid:
        right = pivot_position

    return left, right


def half(data, n):
    value = data[n // 2]
    for i in range(n//2, n):
        if data[i] < value:
            value = data[i]

    return value


def median(data, n):
    left = 0
    right = n - 1
    mid = (left + right) // 2

    while True:
        pivot_position = split(data, left, right)
        print("pivot_position:", pivot_position)
        print("mid: ", mid)

        if pivot_position == mid:
            break

        else:
            left, right = split_range(pivot_position, mid, left, right)

    if n % 2 == 1:
        return data[mid]
    else:
        return (data[mid] + half(data, n)) // 2


num = int(input())
systolic = list(map(int, input().split()))
diastolic = list(map(int, input().split()))

sy_average = average(systolic, num)
dia_average = average(diastolic, num)
sy_median = median(systolic, num)
dia_median = median(diastolic, num)
print(sy_average, dia_average, sy_median, dia_median, sep='\n')
