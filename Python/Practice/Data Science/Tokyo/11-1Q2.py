import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


url = "https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data"

data = pd.read_csv(url, header=None, sep=',')

# 給予每個欄位標籤
data.columns = ['Sex', 'Length', 'Diameter', 'Height', 'Whole', 'Shucked', 'Viscera', 'Shell', 'Rings']
# print(data.head())
sns.pairplot(data)

plt.show()
