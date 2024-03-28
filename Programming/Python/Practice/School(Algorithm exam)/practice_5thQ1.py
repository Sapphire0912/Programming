def Frequency(arr):
    total = [0] * 16
    target = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

    for k in arr:
        index = target.index(k)
        total[index] += 1
    return total


if __name__ == '__main__':
    MD5 = str(input())
    length = len(MD5)

    count = Frequency(MD5)
    max_count = 0
    for i in range(16):
        max_count = max(count)
        if max_count <= 1:
            break

        for j in range(16):
            if count[j] == max_count:
                if j <= 9:
                    print(j, end='')
                else:
                    print(chr(j + ord('A') - 10), end="")
                count[j] = 1
    print()



