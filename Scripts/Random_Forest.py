from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import cross_val_score


def random_forest(features, labels, test_features, test_labels):
    print("-----------Random Forest------------")
    print("\n")
    count = 0
    total = 0
    clf = RandomForestClassifier(max_depth=9, min_samples_split=10, min_samples_leaf=1, random_state=0)
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
    clf = RandomForestClassifier(max_depth=20, min_samples_split=10, min_samples_leaf=1, random_state=0)
    precision = cross_val_score(clf, features, labels, cv=10, scoring='precision')
    recall = cross_val_score(clf, features, labels, cv=10, scoring='recall')
    f1score = cross_val_score(clf, features, labels, cv=10, scoring='f1_macro')
    print("Precision: " + str(precision.mean()))
    print("Recall: " + str(recall.mean()))
    print("F1 Macro: " + str(f1score.mean()))

    print("*" * 50)
    print("\n")