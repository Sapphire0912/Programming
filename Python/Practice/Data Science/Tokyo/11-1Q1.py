from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def draw_images(show=False):
    fig, axes = plt.subplots(10, 10, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []}, gridspec_kw=dict(hspace=0.1, wspace=0.3))
    for i, ax in enumerate(axes.flat):
        ax.imshow(digits.images[i], cmap='binary', interpolation='nearest')
        ax.text(0.05, 0.05, str(digits.target[i]), transform=ax.transAxes, color='green')
    if show:
        plt.show()


digits = load_digits()
data, target = digits.data, digits.target
# draw_images(True)

x_train, x_test, y_train, y_test = train_test_split(data, target, stratify=target, random_state=0)

# 使用不同的模型來預測, 並判斷哪種分類器較優
models = [LogisticRegression(max_iter=1000), LinearSVC(), DecisionTreeClassifier(), KNeighborsClassifier(n_neighbors=3),
          RandomForestClassifier()]
for model in models:
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    confusion = confusion_matrix(y_test, y_pred)
    print('confusion matrix')
    print(confusion)
    print('train:', model.__class__.__name__, model.score(x_train, y_train))
    print('test:', model.__class__.__name__, model.score(x_test, y_test))
    print(f'Accuracy: {accuracy_score(y_pred, y_test)}')
    print('===========================================================\n')
