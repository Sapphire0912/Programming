import tensorflow as tf
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0,2"  # 使用第一張和第三張顯卡
print(tf.__version__)
