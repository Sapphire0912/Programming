import numpy as np
import Cconv
from ctypes import *
import cv2

src = np.random.randint(0, 256, (600, 800))
print(src.dtype)
Cconv.U(41, 80, 92, 143, 160)
Cconv.thresconv(src)

result = Cconv.cvar.result
addr = c_int * 800
addr = addr * 600
p = np.array(addr.from_address(int(result))).astype(np.uint8)

print(Cconv.cvar.result)
print(p.dtype)

cv2.imshow('p', p)
cv2.waitKey(0)

# read value
# u = Cconv.cvar.u
# addr = c_double * 256
# p = list(addr.from_address(int(u)))
# print(p)

# 將 src <- numpy.ndarray 轉成 C 語言的 2d pointer
# 轉成 tuple
# tuple_src = tuple(map(tuple, src))

# 建立 C 語言指標
# double_ptr1d = POINTER(c_double)
# double_ptr2d = POINTER(double_ptr1d)

# 指標位址
# ptr_arr = double_ptr1d * 600
# arr1d = c_double * 800
# arr2d = arr1d * 600

# 2D 指標
# src_arr2d = arr2d(*tuple_src)
# src_ptr2d = cast(
#     ptr_arr(
#         *(cast(y, double_ptr1d) for y in src_arr2d)
#     ), double_ptr2d
# )
# res = Cconv.thresconv(src_ptr2d)
# print(res)

