from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split as tts
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score


iris = load_iris()
x, y = iris.data, iris.target

x_train, x_test, y_train, y_test = tts(x, y, test_size=0.2)

c = 1
gamma = 'auto'
kernel = 'linear'

model = SVC(kernel=kernel, C=c, gamma=gamma)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
print(confusion_matrix(y_pred, y_test))
print(accuracy_score(y_pred, y_test))
