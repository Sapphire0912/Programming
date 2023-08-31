import threading
import numpy as np
import time
from queue import Queue

st = time.time()


def job(n, q):
    total = 0
    for i in n:
        total += i
    q.put(total)


def multi_thread():
    d1 = np.arange(1, 110000)
    d2 = np.arange(110000, 210000)
    d3 = np.arange(210000, 310000)
    # d4 = np.arange(310000, 410000)
    datas = [d1, d2, d3]
    q = Queue()

    all_thread = list()
    for i in range(3):
        thread = threading.Thread(target=job, args=(datas[i], q))
        thread.start()
        all_thread.append(thread)

    for t in all_thread:
        t.join()

    res = 0
    for _ in range(len(all_thread)):
        res += q.get()
    print(res)


multi_thread()

end = time.time()
print('threading spend time: ', end-st)  # 0.037891387939453125


def main():
    tot = 0
    st = time.time()
    x = np.arange(1, 310000)
    for i in x:
        tot += i
    end = time.time()
    print('main spend time: ', end-st)  # 0.03889632225036621


# main()
