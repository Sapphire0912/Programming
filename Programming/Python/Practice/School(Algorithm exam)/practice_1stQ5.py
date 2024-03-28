def GetFirst(num, n):
    M = int(num[-1])
    M %= n
    return num[M - 1]


def bubble(n, num):
    for i in range(n):
        for j in range(n-1):
            if(int(num[j]) > int(num[j+1])):
                temp = num[j]
                num[j] = num[j+1]
                num[j+1] = temp
    return num


if __name__ == '__main__':
    one = list(map(str, input().rstrip().split()))
    two = list(map(str, input().rstrip().split()))
    three = list(map(str, input().rstrip().split()))

    one = bubble(6, one)
    print("三獎為: "+str(one[0])+" "+str(one[1])+" "+str(one[2])+" "+str(one[3])+" "+str(one[4])+" "+str(one[5]))
    two = bubble(4, two)
    print("二獎為: "+str(two[0])+" "+str(two[1])+" "+str(two[2])+" "+str(two[3]))
    three = bubble(2, three)
    print("一獎為: "+str(three[0])+" "+str(three[1]))

    allno = []
    for i in range(6):
        allno.append(one[i])
    for i in range(4):
        allno.append(two[i])
    for i in range(2):
        allno.append(three[i])

    allno = bubble(12, allno)
    first = GetFirst(allno, 12)
    print("首獎為: " + str(first))
