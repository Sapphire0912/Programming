def RemoveDuplicates(data):
    new_data = []
    for k in range(len(data)):
        if data[k] not in new_data:
            new_data.append(data[k])

    return len(new_data)


if __name__ == '__main__':
    m = int(input())

    for i in range(m):
        n = int(input())
        data = [int(d) for d in input().split(' ')]
        print('count' + str(i+1) + ': ' + str(RemoveDuplicates(data)))
