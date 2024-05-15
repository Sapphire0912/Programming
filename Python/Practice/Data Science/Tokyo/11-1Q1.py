from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
import sklearn
import numpy as np
import pandas as pd
import scipy as sp
import time
import matplotlib as mpt
import matplotlib.pyplot as plt
import seaborn as sns


def draw_images(show=False):
    plt.figure(figsize=(12, 2))
    for label, img in zip(digits.target[:10], digits.images[:10]):
        plt.subplot(1, 10, label + 1)
        plt.axis('off')
        plt.imshow(img, cmap=plt.cm.gray_r, interpolation='nearest')
        plt.title('Number:{0}'.format(label))

    if show:
        plt.show()


digits = load_digits()
data, target = digits.data, digits.target

x_train, x_test, y_train, y_test = train_test_split(data, target, stratify=target, random_state=0)
