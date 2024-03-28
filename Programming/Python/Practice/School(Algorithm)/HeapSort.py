def MaxHeapify(A, i):
    size = len(A)
    Left = 2 * i + 1
    Right = 2 * i + 2

    largest = i  # default: largest = i
    if Left < size and A[Left] > A[i]:
        largest = Left
    else:
        largest = i

    if Right < size and A[Right] > A[largest]:
        largest = Right

    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        MaxHeapify(A, i)


def HeapSort(A):
    size = len(A)

    # build max-heap tree
    for i in range(size//2, -1, -1):
        MaxHeapify(A, i)

    pass


data = [16, 14, 10, 8, 7, 9, 3, 2, 4, 1]
