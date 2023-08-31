def assign(weight, no, point, limit):
    weight = weight[point:]
    goods = 0
    lst = list()
    for w in range(len(weight)):
        if goods + weight[w] <= limit:
            goods += weight[w]
            lst.append(point + 1)
            point += 1
        else:
            break

    return lst, point


if __name__ == '__main__':
    cold_limit = int(input())
    normal_limit = int(input())

    cold_no = int(input())
    cold_weight = list(map(int, input().rstrip().split()))

    normal_no = int(input())
    normal_weight = list(map(int, input().rstrip().split()))

    cold_point = 0
    normal_point = 0
    result = []
    while cold_point < cold_no or normal_point < normal_no:
        if cold_point < cold_no:
            cold_pack, cold_point = assign(cold_weight, cold_no, cold_point, cold_limit)
            cj = ""
            for ci in cold_pack:
                cj = cj + "C" + str(ci)
        else:
            cj = 0
            cold_point += 1

        if normal_point < normal_no:
            normal_pack, normal_point = assign(normal_weight,normal_no,normal_point,normal_limit)
            nj = ""
            for ni in normal_pack:
                nj = nj + "N" + str(ni)
        else:
            nj = 0
            normal_point += 1

        result.append(str(cj) + " " + str(nj))

    print(len(result))
    for i in result:
        print(i)

