from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

# Loading the toy dataset from sklearn
iris = datasets.load_iris()

X = iris.data
Y = iris.target
clf = RandomForestClassifier()
clf.fit(X, Y)

# Saving the model
import pickle
pickle.dump(clf, open('iris_clf.pkl', 'wb'))