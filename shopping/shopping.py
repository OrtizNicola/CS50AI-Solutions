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


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Create structures to modify the types of the values depending
    # on the variable
    floats = tuple([1] + [3] + list(range(5, 10)))
    integers = tuple([0] + [2] + [4] + list(range(11, 15)))
    mapping = {
        'Jan': 0,
        'Feb': 1,
        'Mar': 2,
        'Apr': 3,
        'May': 4,
        'June': 5,
        'Jul': 6,
        'Aug': 7,
        'Sep': 8,
        'Oct': 9,
        'Nov': 10,
        'Dec': 11,
        "TRUE": 1,
        "Returning_Visitor": 1,
        "FALSE": 0,
        "New_Visitor": 0,
        "Other": 0
    }

    with open('shopping.csv', 'r') as f:
        reader = csv.reader(f)
        # We dont use the line with the variables names
        next(reader)
        evidence = []
        labels = []
        for line in reader:
            obs = []
            # Modify the evidence depending on the vaiable
            # Change everything to numbers!
            for i, value in enumerate(line[:17]):
                if i in floats:
                    obs.append(float(value))
                elif i in integers:
                    obs.append(int(value))
                else:
                    obs.append(mapping[value])      
            evidence.append(obs)
            labels.append(0 if line[17] == "FALSE" else 1)
    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Create the model with scikit-learn
    model = KNeighborsClassifier(n_neighbors = 1)
    # Train it
    model.fit(evidence, labels)
    # Return it
    return(model)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    correct1 = 0
    correct0 = 0
    n = len(labels)
    # Amount of people who bougth something in the training data
    num1 = labels.count(1)
    # Amount of people who didn't buy anything
    num0 = n - num1
    for i in range(n):
        # If we predicted the right value
        if predictions[i] == labels[i]:
            # We count depending if it was a 0 or a 1
            if labels[i] == 1:
                correct1 += 1
            else: 
                correct0 += 1
    # Calculate the rate of right predictions for 1's and 0's
    sensitivity = correct1 / num1
    specificity = correct0 / num0
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
