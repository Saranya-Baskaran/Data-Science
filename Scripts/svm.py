from sklearn import svm
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import cross_val_score


def support_vector_machine(features, labels, test_features, test_labels):
    print("-----------SVM------------")
    print("\n")
    clf = svm.SVC()
    clf.fit(features, labels)
    predicted = clf.predict(test_features)

    prf = precision_recall_fscore_support(test_labels, predicted, average=None)

    scores = []
    for i in range(len(prf) - 2):
        scores.append(prf[i][1])

    print("Precision for positive label:" + " " + str(scores[0]))
    print("Recall for positive label:" + " " + str(scores[1]))

    print("\n")

    print("-----------Cross Validation Score:----------- ")
    clf = svm.SVC()
    precision = cross_val_score(clf, features, labels, cv=10, scoring='precision')
    recall = cross_val_score(clf, features, labels, cv=10, scoring='recall')
    f1score = cross_val_score(clf, features, labels, cv=10, scoring='f1_macro')
    print("Precision: " + str(precision.mean()))
    print("Recall: " + str(recall.mean()))
    print("F1 Macro: " + str(f1score.mean()))

    print("*" * 50)
    print("\n")
