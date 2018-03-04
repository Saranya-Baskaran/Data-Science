from sklearn import linear_model
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import cross_val_score


def linear_regression(features, labels, test_features, test_labels):
    print("-----------Linear Regression------------")
    print("\n")
    linreg = linear_model.LinearRegression()
    linreg.fit(features, labels)
    linear_predict = linreg.predict(test_features)

    for val in zip(range(len(linear_predict))):
        if linear_predict[val] >= 0.5:
            linear_predict[val] = 1
        else:
            linear_predict[val] = 0

    prf = precision_recall_fscore_support(test_labels, linear_predict, average=None)

    scores = []
    for i in range(len(prf) - 2):
        scores.append(prf[i][1])

    print("Precision for positive label:" + " " + str(scores[0]))
    print("Recall for positive label:" + " " + str(scores[1]))

    print("\n")

    # print("-----------Cross Validation Score:-----------")
    # linreg = linear_model.LinearRegression()
    # precision = cross_val_score(linreg, features, labels, cv=10, scoring='precision')
    # recall = cross_val_score(linreg, features, labels, cv=10, scoring='recall')
    # f1score = cross_val_score(linreg, features, labels, cv=10, scoring='f1_macro')
    # print("Precision: " + str(precision.mean()))
    # print("Recall: " + str(recall.mean()))
    # print("F1 Macro: " + str(f1score.mean()))
    #
    # print("*" * 50)
