from CArray import *
import ctypes
import numpy as np

lst = [0] * 5
lst[0], lst[1] = 10, 20
lst[2], lst[3], lst[4] = 30, 40, 50

# lst = [2, 5, 6, 10, 24, 90, 100, 80, 255]
# lst = np.array([2, 5, 6, 10, 24], np.int)  # np array 會有問題

a = intArray(len(lst))
for i in range(len(lst)):
    a[i] = lst[i]
handleArray(a, len(lst))

res = cvar.c
addr = ctypes.c_int * len(lst)
res = list(addr.from_address(int(res)))
print(res)

