import pickle
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, pearsonr, zscore
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier

# Read data from csv file.
dataframe = pd.read_csv("breastcancerdata.csv")
# Explore our data.
dataframe.info()

# Cleaning our data.
data_modified = dataframe.drop(labels=["Unnamed: 32", "id"], axis=1)
data_modified['diagnosis'] = data_modified['diagnosis'].map({'M': 1, 'B': 0})

# Remove outliers.
z_scores = zscore(data_modified)
abs_z_scores = np.abs(z_scores)
filtered_entries = (abs_z_scores < 3).all(axis=1)
data_modified = data_modified[filtered_entries]

# split our data into features and outcome.
x = data_modified.drop("diagnosis", axis=1)
y = data_modified["diagnosis"]


# A function to select the best features by checking their correlation.
def manualFeatureSelection(features, outcome, r=0.76, pro=0.01, corrType='p'):
    # First filter
    # Check correlation between all features and the outcome.
    x1 = []
    for i in features:
        if corrType == 's':
            rho, p = spearmanr(features[str(i)], outcome)
        else:
            rho, p = pearsonr(features[str(i)], outcome)

        if (abs(rho) > r) and (p < pro):
            x1.append(i)
    x2 = features[x1]
    # -----------------------------------------------------------------------------
    # Second filter
    # Check correlation between all features and each other to eliminate redundant features.

    corrColumns = set()  # Set of all the names of correlated columns

    if corrType == 's':
        corr_matrix = x2.corr(method='spearman')
    else:
        corr_matrix = x2.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > r:  # we are interested in absolute coeff value
                colname = corr_matrix.columns[i]  # getting the name of column
                corrColumns.add(colname)
    return list(corrColumns)


# Best manual features selected after many experiments were:
# ['perimeter_worst', 'area_worst', 'radius_worst', 'concave points_worst']
x_featuresManual = ['perimeter_worst', 'area_worst', 'radius_worst', 'concave points_worst']
for i in x_featuresManual:
    print(np.mean(x[x_featuresManual]))

# Split data into (70%) train data and (30%) test data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)


# As the best model which was used is the random forest model with applying GridSearchCV to tune its hyperparameters,
# To avoid overfitting, And selecting manual selected features, After many experiments.


breastCancerModel = RandomForestClassifier(max_depth=3,
                                           max_features=2,
                                           min_samples_split=25,
                                           n_estimators=500)

breastCancerModel.fit(x_train[x_featuresManual], y_train)

print(accuracy_score(y_test, breastCancerModel.predict(x_test[x_featuresManual])))
score = cross_val_score(breastCancerModel, x, y, cv=KFold(n_splits=5))
print("Cross Validation Scores are {}".format(score))
print("Average Cross Validation score :{}".format(score.mean()))

# Make a pickle file of our model.
pickle.dump(breastCancerModel, open("model.pkl", "wb"))