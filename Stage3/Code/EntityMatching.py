import py_entitymatching as em
import csv
import os
import pandas as pd
import py_entitymatching as em

# reading cleaned csv files from stage 2
A = em.read_csv_metadata('./filmcrave1.csv', key='id')
B = em.read_csv_metadata('./imdb1.csv', key='id')

# Creating instance for overlap blocker.
ob = em.OverlapBlocker()

# Overlapping on Title. (Atleast 1 word match) - [Performed better than 3-gram]
overlap_candidate = ob.block_tables(A, B, 'Title', 'Title', word_level=True, overlap_size=1, rem_stop_words=False, 
                    l_output_attrs=['Title', 'Overall Rating', 'Year', 'Genre', 'Directors', 'Actors'], 
                    r_output_attrs=['Title', 'Overall Rating', 'Year', 'Genre', 'Directors', 'Actors'],
                    show_progress=False)

# Filtering previous stage blocker output further by matching atleast 1 word in directors
overlap_candidate1 = ob.block_candset(overlap_candidate, 'Directors', 'Directors', word_level=True, overlap_size=1, show_progress=False)

# Creating instance for attribute blocker
ab = em.AttrEquivalenceBlocker()

# Blocking previous level blocker using matching year attribute
attribute_candidate = ab.block_candset(overlap_candidate1, 'Year', 'Year', show_progress=False)

# Randomly sampling 500 records from the candidate tuple pairs
sample = em.sample_table(attribute_candidate, 500)

# Storing this sample for labelling.
sample.to_csv("Sampleset.csv")

# Opening the csv file and cleaning and converting to new CSV File
with open('./Sampleset.csv', 'r', encoding='utf-8', errors='ignore') as infile, open('./Sampleset1.csv', 'w') as outfile:
     inputs = csv.reader(infile)
     outputs = csv.writer(outfile)

     for index, row in enumerate(inputs):
         outputs.writerow(row)

# Read in the labelled dataset        
G = em.read_csv_metadata("./Sampleset1.csv", key='_id', 
                         fk_ltable='ltable_id', fk_rtable='rtable_id',
                         ltable=A, rtable=B)

# Splitting the data into training and testing portions. 
split = em.split_train_test(G, train_proportion=0.5, random_state=0)

# Training and testing set splits
train_set = split['train']
test_set = split['test']

# Initialising all ML algos
dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')

# Generating features for training
features = em.get_features_for_matching(A, B, validate_inferred_attr_types=False)

# Extracting feature vectors to train and create model
H = em.extract_feature_vecs(train_set, 
                            feature_table=features, 
                            attrs_after='label',
                            show_progress=False)

H.head()

# Checking if any value is null
any(pd.notnull(H))

# We found null values. Hence, used impute_table to fill up the other values with strategy - mean.
H = em.impute_table(H, 
                exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'label'],
                strategy='mean')

# Running select matcher step to run all possible algos and pick the best ML
result = em.select_matcher([dt, rf, svm, ln, lg], table=H, 
        exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'label'],
        k=5,
        target_attr='label', metric_to_select_matcher='f1', random_state=0)

# Showing cross validation statistics
result['cv_stats']

# Choosing Linear Regression as it has highest f1-score.
dt = em.DTMatcher(name='LinReg', random_state=0)

dt.fit(table=H, 
       exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'label'], 
       target_attr='label')

# Extracting feature vectors for test_set
L = em.extract_feature_vecs(test_set, feature_table=features,
                            attrs_after='label', show_progress=False)
# Checking for null values in test_Set
any(pd.notnull(L))

# Filling null values with mean of the column
L = em.impute_table(L, 
                exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'label'],
                strategy='mean')

# Predicting on the test set
predictions = dt.predict(table=L, exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'label'], 
              append=True, target_attr='predicted', inplace=False, return_probs=True,
                        probs_attr='proba')

predictions[['_id', 'ltable_id', 'rtable_id', 'predicted', 'proba']].head()

# Evaluating the matches and printing summary out
eval_result = em.eval_matches(predictions, 'label', 'predicted')
em.print_eval_summary(eval_result)


