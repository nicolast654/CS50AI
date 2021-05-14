import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

    # test = load_data(sys.argv[1])
    # print(test[0][0], test[1][0])

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer --> index 0
        - Administrative_Duration, a floating point number --> index 1
        - Informational, an integer --> index 2
        - Informational_Duration, a floating point number --> index 3
        - ProductRelated, an integer --> index 4
        - ProductRelated_Duration, a floating point number --> index 5
        - BounceRates, a floating point number --> index 6
        - ExitRates, a floating point number --> index 7
        - PageValues, a floating point number --> index 8
        - SpecialDay, a floating point number --> index 9
        - Month, an index from 0 (January) to 11 (December) --> index 10
        - OperatingSystems, an integer --> index 11
        - Browser, an integer --> index 12
        - Region, an integer --> index 13
        - TrafficType, an integer --> index 14
        - VisitorType, an integer 0 (not returning) or 1 (returning) --> index 15
        - Weekend, an integer 0 (if false) or 1 (if true) --> index 16

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # list of indexs that have elements that should be converted to int or float
    int_list = [0,2,4,11,12,13,14]
    float_list = [1,3,5,6,7,8,9]


    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        data = ([], [])
        #data = (evidence,labels)
        for row in reader:
            data[0].append(row[:-1])
            data[1].append(row[-1])
            
        # loop through the list and change the type of the value depending on the index
        for cell in data[0]:
            for i in range(len(cell)):
                if i in int_list:
                    cell[i] = int(cell[i])
                elif i in float_list:
                    cell[i] = float(cell[i])
                elif i == 10:
                    months  = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    for month in months:
                        if cell[10] == month:
                            cell[10] = months.index(month)
                            break
                elif i == 15:
                    if cell[15] == 'Returning_Visitor':
                        cell[15] = 1
                    else:
                        cell[15] = 0
                elif i == 16:
                    if cell[16] == 'FALSE':
                        cell[16] = 0
                    else:
                        cell[16] = 1

        for i in range(len(data[1])):
            if data[1][i] == 'TRUE':
                data[1][i] = 1
            else:
                data[1][i] = 0

    return data

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0.0
    specificity = 0.0

    true_positive_labels = 0
    true_positive_prediction = 0

    true_negative_labels = 0
    true_negative_predictions = 0

    for i in range(len(labels)):
        if labels[i] == 1:
            true_positive_labels +=1 # count the number of true labels
            true_positive_prediction += predictions[i] # or 1 or 0 depending on if it was correct or no
        else:
            true_negative_labels += 1 # count the number of negative labels
            true_negative_predictions += 1 - predictions[i] # add 0 if it was 1 and 1 if it was 0

    sensitivity = float(true_positive_prediction/true_positive_labels)
    specificity = float(true_negative_predictions/true_negative_labels)
    
    return (sensitivity,specificity)

if __name__ == "__main__":
    main()

























