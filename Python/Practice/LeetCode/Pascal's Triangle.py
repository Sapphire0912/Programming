# Given an integer numRows, return the first numRows of Pascal's triangle.

def generate(numRows):
    res = list()

    for index in range(0, numRows):
        curr = [1] * (index + 1)

        for i in range(1, index):
            curr[i] = res[index-1][i-1] + res[index-1][i]
        res.append(curr)
    return res


print(generate(5))
