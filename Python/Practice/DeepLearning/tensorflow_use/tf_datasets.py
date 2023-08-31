import tensorflow as tf
import tensorflow_datasets as tfds

# url: https://www.tensorflow.org/datasets/catalog/overview
print(tfds.list_builders())  # tensorflow 的 datasets
print(len(tfds.list_builders()))

# 使用時要考慮如把讀進來的資料轉成正確的輸入格式(numpy 數據)
# 會因為不同資料集合而有不同的處理方式
