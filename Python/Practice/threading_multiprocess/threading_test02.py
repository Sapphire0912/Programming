import threading
import numpy as np
import time

total = 0
st = time.time()


def job(n):
    global total
    for i in n:
        total += i


def multi_thread():
    d1 = np.arange(1, 11000)
    d2 = np.arange(11000, 21000)
    d3 = np.arange(21000, 31000)
    d4 = np.arange(31000, 41000)
    datas = [d1, d2, d3, d4]

    all_thread = list()
    for i in range(4):
        thread = threading.Thread(target=job, args=(datas[i],))
        thread.start()
        all_thread.append(thread)

    for t in all_thread:
        t.join()
    print('last: ', total)


# multi_thread()
#
end = time.time()
print('threading spend time: ', end-st)  # 0.006089448928833008


def main():
    tot = 0
    st = time.time()
    x = np.arange(1, 41000)
    for i in x:
        tot += i
    end = time.time()
    print('main spend time: ', end-st)


main()
# GIL問題?? Q. 若所有執行緒都改變同個變數會等於順序執行
