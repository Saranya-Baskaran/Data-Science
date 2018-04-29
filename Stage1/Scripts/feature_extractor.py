import os
import string
import re
import fileinput
import nltk
import collections

from decisiontree import decision_tree_classifier
from Random_Forest import random_forest
from Logistic_Regression import logistic_regression
from svm import support_vector_machine
from Linear_Regression import linear_regression

from all_lists import *

from Scripts.all_lists import stop_words, location_tenders, prepositions, substr, followed_by, nonlocation_nouns

pos_tag_dict = {}


def check_capitalised(word):
    words = word.split()
    for w in words:
        if not w[0].isupper():
            return False
    return True


def check_in_followed_by(word, followed_by):
    words = word.split()

    if len(words) == 1:
        if words[0].lower() in followed_by:
            return True
        else:
            return False
    else:
        if words[0].lower() in followed_by:
            return True
        else:
            return False


def check_in_preposition(word, prepositions):
    words = word.split()

    if len(words) == 1:
        if words[0].lower() in prepositions:
            return True
        else:
            return False
    else:
        if words[1].lower() in prepositions:
            return True
        else:
            return False


def check_in_stopwords(word, stop_words):
    words = word.split()
    for w in words:
        if w.lower() in stop_words:
            return True
    return False


def check_if_location_tender(word, location_tenders, unmod_word):
    words = word.split()
    unmod_words = unmod_word.split()
    if len(words) == 1:
        if words[0] in location_tenders:
            return True
        else:
            return False

    else:
        if words[0] in location_tenders and pos_tag_dict[words[1]] == 7:
            return True
        else:
            return False


def check_if_substr(word, substr):
    words = word.split()

    for w in substr:
        if words[-1].endswith(w):
            return True
    return False


def gen_labels(words):
    labels = []
    prev = []
    follow = []
    location = []
    non_location = []
    for i in range(len(words)):
        word = words[i].split()
        if len(word) > 1:

            if word[0].startswith('#L') and not word[0].endswith('#L') and not word[1].startswith('#L') and word[
                1].endswith('#L'):
                labels.append(int(1))

            else:
                non_location.append(words[i])
                labels.append(int(0))

        else:
            if word[0].startswith('#L') and word[0].endswith('#L'):

                prev.append(words[i - 1])

                location.append(words[i])
                follow.append(words[i + 1])

                labels.append(int(1))
            else:
                non_location.append(words[i])
                labels.append(int(0))

    return labels


def pos_tag_label(tag):
    pos_tag = {',': 0, '.': 6, 'CC': 5, 'IN': 1, 'POS': 0, 'NN': 2, 'NNP': 7, 'VB': 3, 'VBD': 3,
               'VBG': 3, 'VBN': 3, 'VBP': 3, 'VBZ': 3, 'JJ': 4, 'JJR': 4, 'JJS': 4}

    if tag in pos_tag:
        return pos_tag[tag]
    else:
        return 0


def generating_features(all_words, feature_index, feature, labels, prepositions, stop_words, location_tenders, substr,
                        followed_by, nonlocation_nouns):
    follow = []
    unmod_words = list(all_words)
    previous_tags = []
    follow_tags = []

    for i in range(len(all_words) - 1):
        all_words[i] = re.sub(r"#L", "", all_words[i])

    for i in range(len(all_words)):
        if labels[i] == 1:
            previous_tags.append(pos_tag_dict[all_words[i - 1]])
            follow_tags.append(pos_tag_dict[all_words[i + 1]])

    for i in range(len(all_words)):

        temp_vector = []

        prev_word = ""
        word = all_words[i]
        next_word = ""
        prev_tag = 0
        prev_prev_tag = 0
        current_tag = 0
        next_tag = 0
        next_next_tag = 0

        if i != 0:
            prev_word = all_words[i - 1]

        if i != len(all_words) - 1:
            next_word = all_words[i + 1]

        if i >= 2:
            prev_prev_tag = pos_tag_dict[all_words[i - 2]]

        if i < len(all_words) - 2:
            next_next_tag = pos_tag_dict[all_words[i + 2]]

        if prev_word != "":
            prev_tag = pos_tag_dict[prev_word]
        if next_word != "":
            next_tag = pos_tag_dict[next_word]

        current_tag = pos_tag_dict[word]

        """
        Feature 1. Check if first word in the string is uppercase
        
        """
        if check_capitalised(word) is True:
            temp_vector.append(int(1))
        else:
            temp_vector.append(int(0))

        """
        Feature 2. If previous word is preposition
        
        """

        if prev_word != "" and check_in_preposition(all_words[i - 1], prepositions) is True:
            temp_vector.append(int(1))
        else:
            temp_vector.append(int(0))

        """
        Feature 3. If one of the words is a stop word
        
        """
        if check_in_stopwords(all_words[i], stop_words):
            temp_vector.append(int(1))
        else:
            temp_vector.append(int(0))

        """
        Feature 4. If previous word is a location tending word
        
        """
        temp = word.split()

        if len(temp) == 2 and check_if_location_tender(all_words[i], location_tenders, unmod_words[i]):
            temp_vector.append(int(1))
        elif len(temp) == 1 and prev_word != "" and pos_tag_dict[word] == 7 and check_if_location_tender(
                all_words[i - 1], location_tenders, unmod_words[i - 1]):
            temp_vector.append(int(1))
        else:
            temp_vector.append(int(0))

        """
        Feature 5. If it contains substr

        """
        if check_if_substr(all_words[i], substr):
            temp_vector.append(int(1))
        else:
            temp_vector.append(int(0))

        """
        Feature 6. Followed By
        
        """

        if i != len(all_words) - 1 and next_word != "" and check_in_followed_by(all_words[i + 1],
                                                                                followed_by) is True:

            temp_vector.append(int(1))
        else:
            if labels[i] == 1:
                # print(word, next_word)
                follow.append(next_word)
            temp_vector.append(int(0))

        """
        Feature 7, 8, 9. Pos tag Prev word, current, next
              
        """

        temp_vector.append(prev_tag)

        if current_tag == 7:
            temp_vector.append(int(1))
        else:
            temp_vector.append(int(0))

        temp_vector.append(next_tag)

        """
        Feature 10. First word
        
        """
        if prev_word != "" and current_tag == 7 and prev_word == ".":
            temp_vector.append(int(1))
        else:
            temp_vector.append(int(0))

        """
        Feature 11. Last word
        
        """
        if next_word != "" and current_tag == 7 and next_word == ".":
            temp_vector.append(int(1))
        else:
            temp_vector.append(int(0))

        """
        Feature 12. is in unwanted bag of nouns
        
        """
        if word in nonlocation_nouns:
            temp_vector.append(int(1))
        else:
            temp_vector.append(int(0))

        """
        Feature 13. Prefix . and preposition Suffix NN OR verb
        
        """
        if prev_tag == 1 or next_tag == 0:
            temp_vector.append(int(1))
        else:
            temp_vector.append(int(0))

        feature.append(temp_vector)

        """
        Feature 14 Abbreviations handler
        
        """
        temp = word.split()

        if len(temp) == 1 and len(temp[0]) == 2:
            abb = temp[0].upper()
            if abb == temp[0]:
                temp_vector.append(int(1))
            else:
                temp_vector.append(int(0))
        else:
            temp_vector.append(int(0))

        feature_index += 1

    return feature


def main():
    directory = "../Data/training_data"
    test_dir = "../Data/testing_data"

    test_features = []
    test_uni = []
    test_bi = []
    test_labels = []
    feature_vectors = []
    labels = []
    temp_features = []
    temp_labels = []
    unigrams = []
    bigrams = []

    feature_index = 0

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            f = fileinput.input(os.path.join(directory, filename))

            for line in f:
                """ 
                    Stripping new line
                """
                line = line.rstrip('\n')

                line = line.replace(string.punctuation.replace('#', ''), '')

                line = " ".join(line.split())
                modified_line = line.replace('#L', '')
                tokens = modified_line.split()

                tag = nltk.pos_tag(tokens)

                for i in range(len(tag)):

                    if tag[i][0] not in pos_tag_dict:
                        modified_tag = pos_tag_label(tag[i][1])
                        pos_tag_dict[tag[i][0]] = modified_tag

                """ 
                Splitting on delimiter. Better to include stopwords
                
                """
                for word in line.split():
                    if word == "" or word == "#L":
                        continue
                    unigrams.append(word)

    for filename in os.listdir(test_dir):
        if filename.endswith(".txt"):
            f = fileinput.input(os.path.join(test_dir, filename))

            for line in f:
                """ 
                 Stripping new line
                 
                """
                line = line.rstrip('\n')
                line = line.replace(string.punctuation.replace('#', ''), '')
                modified_line = line.replace('#L', '')
                tokens = modified_line.split()

                tag = nltk.pos_tag(tokens)

                for i in range(len(tag)):

                    if tag[i][0] not in pos_tag_dict:
                        modified_tag = pos_tag_label(tag[i][1])
                        pos_tag_dict[tag[i][0]] = modified_tag

                """ 
                Splitting on delimiter. Better to include stopwords

                """
                for word in line.split():
                    if word == "" or word == "#L":
                        continue
                    test_uni.append(word)

    """
    Only form bigrams with unigrams that are not punctuations
    
    """

    for i in range(len(unigrams) - 1):
        bigrams.append(unigrams[i] + " " + unigrams[i + 1])
        mod_bigram = bigrams[-1].replace("#L", "")
        pos_tag_dict[mod_bigram] = 0

    all_words = unigrams + bigrams

    """
    doing nltk pos_tagging
    
    """
    labels = gen_labels(all_words)
    # print("Training")
    # print(collections.Counter(labels))

    features = generating_features(all_words, feature_index, feature_vectors, labels, prepositions,
                                   stop_words,
                                   location_tenders, substr, followed_by, nonlocation_nouns)

    """
    Only form bigrams with unigrams that are not punctuations
    
    """

    for i in range(len(test_uni) - 1):
        test_bi.append(test_uni[i] + " " + test_uni[i + 1])
        mod_bigram = test_bi[-1].replace("#L", "")
        pos_tag_dict[mod_bigram] = 0

    test_words = test_uni + test_bi

    test_labels = gen_labels(test_words)
    # print("Testing")
    # print(collections.Counter(test_labels))

    test_features = generating_features(test_words, feature_index, temp_features, test_labels, prepositions,
                                        stop_words,
                                        location_tenders, substr, followed_by, nonlocation_nouns)

    decision_tree_classifier(features, labels, test_features, test_labels)
    random_forest(features, labels, test_features, test_labels)
    support_vector_machine(features, labels, test_features, test_labels)
    logistic_regression(features, labels, test_features, test_labels)
    linear_regression(features, labels, test_features, test_labels)


if __name__ == "__main__":
    main()
