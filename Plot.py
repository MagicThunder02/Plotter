# Warning: this program has no comments.
# In order to know what it does
# and how it works,
# you have to contact the developer

import matplotlib.pyplot as plt
import mglearn
from sklearn.datasets import load_breast_cancer
# from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
# from sklearn.datasets import load_boston
# from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

__author__ = "Carlo Federico Vescovo"

__developer__ = "Carlo Federico Vescovo"

__credits__ = ["Carlo Federico Vescovo"]

__license__ = "MIT"

__maintainer__ = "Carlo Federico Vescovo"

__email__ = "dev@cfvmail.cf"

__status__ = "Development"


if __name__ == "__main__":

    cancer = load_breast_cancer()

    X_train, X_test, y_train, y_test = train_test_split(
        cancer.data, cancer.target, stratify=cancer.target, random_state=69)

    lr = Ridge().fit(X_train, y_train)

    train_score = lr.score(X_train, y_train)

    test_score = lr.score(X_test, y_test)

    train_predictions = lr.predict(X_train)

    train_real = y_train

    test_predictions = lr.predict(X_test)

    test_real = y_test

    mglearn.plots.plot_ridge_n_samples()

    plt.show()

    plt.plot(train_real, train_predictions, "rs", test_real, test_predictions, "bs")

    plt.show()

    X, y = mglearn.datasets.make_forge()

    mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
    plt.legend(["Class 0", "Class 1"], loc=4)
    plt.xlabel("First feature")
    plt.ylabel("Second feature")
    print("X.shape: {}".format(X.shape))

    plt.show()

else:
    print("Do not import this file. There are no defs.")
