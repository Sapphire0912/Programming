def PadIn(Box, no):
    Box.append(no)
    return Box


def PadOut(Box):
    return Box[:len(Box)-1]


if __name__ == '__main__':
    global top

    Box = list(map(str, input().rstrip().split()))
    Box.reverse()

    borrow_list = []
    borrow_no = int(input())

    for i in range(borrow_no):
        try:
            borrow_list.append(list(map(str, input().rstrip().split())))
        except EOFError:
            break

    top = len(Box) - 1
    for x in range(len(borrow_list)):
        if borrow_list[x][0] == "In":
            Box = PadIn(Box, borrow_list[x][1])

        if borrow_list[x][0] == "Out":
            Box = PadOut(Box)

    result = ""
    if Box == list():
        print("None")

    else:
        for y in range(len(Box)):
            result = str(result) + Box[len(Box)-y-1] + " "
        print(len(Box))
        print(result)
