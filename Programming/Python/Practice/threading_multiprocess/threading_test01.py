import threading
import time
from queue import Queue
import numpy as np


def job(data, q):
    for i in range(len(data)):
        data[i] = data[i] * 2
    q.put(data)


def multi_thread():
    datasets = np.zeros((10, 10))
    print(datasets)
    q = Queue()

    all_thread = list()

    for i in range(len(datasets)):
        thread = threading.Thread(target=job, args=(datasets[i], q))
        thread.start()
        all_thread.append(thread)
    print('thread 數量: ', len(all_thread))
    for t in all_thread:
        t.join()

    result = list()
    for i in range(len(all_thread)):
        d = q.get()
        print("i: ", i, "data: ", d)
        result.append(d)
    print(result)


multi_thread()
