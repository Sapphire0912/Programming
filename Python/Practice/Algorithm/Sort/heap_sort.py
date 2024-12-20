def heap_sort(lst):
    def sift_down(start, end):
        root = start
        while True:
            child = 2 * root + 1
            if child > end:
                break
            if child + 1 <= end and lst[child] < lst[child + 1]:
                child += 1
            if lst[root] < lst[child]:
                lst[root], lst[child] = lst[child], lst[root]
                root = child
            else:
                break

    for start in range((len(lst) - 2) // 2, -1, -1):
        sift_down(start, len(lst) - 1)
        # print("Start loop: ",lst)

    for end in range(len(lst) - 1, 0, -1):
        lst[0], lst[end] = lst[end], lst[0]
        # print("End loop: ",lst)
        sift_down(0, end - 1)
        # print("End loop: ",lst)
    return lst

if __name__ == "__main__":
    mylist = [20, 9, 100, 0, 55, 3, 11]
    print(heap_sort(mylist))