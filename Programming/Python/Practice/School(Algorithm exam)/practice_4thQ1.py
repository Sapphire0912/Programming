def Match(AdmissionList, student_no, class_list):
    score = 0
    for k in range(len(class_list)):
        if class_list[k] in AdmissionList:
            score += 1

    return score


if __name__ == '__main__':
    list_no = int(input())
    AdmissionList = list(map(str, input().rstrip().split()))

    class_list = list()
    class_no = int(input())
    for i in range(class_no):
        try:
            class_list.append(list(map(str, input().rstrip().split())))
        except EOFError:
            break

    for i in range(class_no):
        Admission = Match(AdmissionList, class_list[i][0], class_list[i][1:])
        print(Admission)
