def GetTaxt(taxi, taxi_len):
    if len(taxi) >= 2:
        return taxi[1:]
    return -1


if __name__ == '__main__':
    passenger_no = int(input())
    passenger = list(map(str, input().rstrip().split()))
    passenger_list = []

    for x in range(len(passenger)):
        if int(passenger[x]) > 4:
            person = passenger[x]
            group = int(person) / 4

            for y in range(int(group)):
                passenger_list.append('4')

            if int(person) % 4 != 0:
                passenger_list.append(str(int(person) % 4))
        else:
            passenger_list.append(passenger[x])

    taxi_no = int(input())
    taxi = list(map(str, input().rstrip().split()))

    for i in range(len(passenger_list)):
        taxi = GetTaxt(taxi, len(taxi))

        if taxi == -1:
            print("waiting")
            break

        if i == len(passenger_list) - 1:
            print(taxi[0])

