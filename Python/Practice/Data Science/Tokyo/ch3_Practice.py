import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"

data = pd.read_csv(url, sep=';')

describe = data.describe()
mode = data.mode().set_index(pd.Index(['mode']))  # dataframe -> set index
var = pd.DataFrame(data.var()).T.set_index(pd.Index(['var']))  # series -> dataframe -> set index
result = pd.concat([describe, mode, var])  # concat

# print(result)
# result.to_csv('datasummary.csv')

correlation = data.corr()
for i in range(len(correlation.columns)):
    correlation.iloc[i, i] = 0

correlation.to_csv('correlation.csv')
