def HammingDistance(x, y):
    # x, y is int
    distance = 0
    xor = x ^ y

    while xor != 0:
        distance += xor & 1
        xor >>= 1
        print(xor)

    return distance


print(HammingDistance(9, 5))
