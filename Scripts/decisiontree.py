from sklearn import tree, svm, linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support
import scipy
import csv
import collections


def decision_tree_classifier(features, labels, test_features, test_labels, all_words, test_words):
    count = 0
    print ("Decision Tree")
    print(collections.Counter(labels))
    print(collections.Counter(test_labels))
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(features, labels)
    predicted = clf.predict(test_features)
    print(collections.Counter(predicted))
    total = 0
    black_list = []
    with open("result.csv", "w") as f:
        f.write("Words,actual label,predicted label,isupper,precedded,stop word,location tendor," +
                "contains,followedby,prev tag,isnoun,next tag,first word,last word,white list,neg bag, prefix suffix, abbreviation" + "\n")

        writer = csv.writer(f)
        for w1, w2, w3, w4 in zip(test_words,test_labels, predicted, test_features):
            if w2 == 0 and w3 == 0:
                continue
            if w2 == 1 and w3 == 0:
                continue
            if w2 == 1 and w3 == 1:
                continue
            #print (w1, w2, w3)

            result = ""
            result = w1 + "," + str(w2) + "," + str(w3) + ", "
            black_list.append(w1)
            for feature in w4:
                #print (str(feature) + ",")
                result += str(feature) + ","
                #print ("\n")
            result += "\n"
            #print(result)
            f.write(result)
            #writer.writerows(w4)

        # for w1, w2, w3, w4 in zip(test_words,test_labels, predicted, test_features):
        #     if w2 == 0 and w3 == 0:
        #         continue
        #     if w2 == 0 and w3 == 1:
        #         continue
        #     if w2 == 1 and w3 == 0:
        #         continue
        #     #print (w1, w2, w3)
        #
        #     result = ""
        #     result = w1 + "," + str(w2) + "," + str(w3) + ", "
        #
        #     for feature in w4:
        #         #print (str(feature) + ",")
        #         result += str(feature) + ","
        #         #print ("\n")
        #     result += "\n"
        #     #print(result)
        #     f.write(result)
        #     #writer.writerows(w4)

    print(collections.Counter(black_list))
    for val1, val2 in zip(test_labels, predicted):
        if val1 == 1:
            total += 1
            if val2 == 1:
                count += 1

    print ("count :", count)
    print ("total: ", total)
    print("ratio:", count / total)

    prf = precision_recall_fscore_support(test_labels, predicted, average=None)

    print (prf)

    print("#" * 20)
    print ("SVM")
    count = 0
    clf = svm.SVC()
    clf.fit(features, labels)
    predicted = clf.predict(test_features)

    for val1, val2 in zip(test_labels, predicted):
        if val1 == 1:
            if val2 == 1:
                count += 1

    print ("count :", count)
    print ("total: ", total)
    print("ratio:", count / total)

    print(precision_recall_fscore_support(test_labels, predicted, average=None))
    print("#" * 20)
    print ("Logistic")
    count = 0
    logreg = linear_model.LogisticRegression()
    logreg.fit(features, labels)
    predicted = logreg.predict(test_features)

    for val1, val2 in zip(test_labels, predicted):
        if val1 == 1:
            if val2 == 1:
                count += 1

    print ("count :", count)
    print ("total: ", total)
    print("ratio:", count / total)

    print(precision_recall_fscore_support(test_labels, predicted, average=None))
    print("#" * 20)

    print ("Random Forest")
    count = 0
    clf = RandomForestClassifier(max_depth=2, random_state=0)
    clf.fit(features, labels)
    predicted = clf.predict(test_features)

    for val1, val2 in zip(test_labels, predicted):
        if val1 == 1:
            if val2 == 1:
                count += 1

    print ("count :", count)
    print ("total: ", total)
    print("ratio:", count / total)

    print(precision_recall_fscore_support(test_labels, predicted, average=None))
    print("#" * 20)