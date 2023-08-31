import math


def cumulative(number, people):
    lst = [int(people[0])]
    for i in range(1, len(people)):
        lst.append(int(lst[i-1]) + int(people[i]))

    return lst


if __name__ == '__main__':
    number = int(input())
    people = list(map(str, input().rstrip().split()))

    interval = cumulative(number,people)

    val = list()
    percent = 0
    for x in range(4):
        percent = (x+1) / 5
        val.append(math.ceil(interval[number-1]*percent))

    result = list()
    for y in range(4):
        for z in range(len(interval)):
            if val[y] <= interval[z]:
                result.append(z+1)
                break

    print(result[0], result[1], result[2], result[3])


