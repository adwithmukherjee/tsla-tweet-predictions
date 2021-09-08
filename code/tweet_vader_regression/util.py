import random
from numpy.core.numeric import tensordot
import pandas as pd

def load_file(file_path, x_var):
    """
    input:
        file_path: the path to the data file
        x_var:
            - for simple linear regression: the name of the independent variable
            - for multiple linear regression: a list of the names of the independent
            variables
            NOTE: to access a column in a pandas dataframe (df), you do
                    df['column_name'].values;
                to access multiple columns, you need df[['column_name1',
                    'column_name2', ..., ]]

    output:
        X: python list of independent variables values
        y: python list of the dependent variable
            values (i.e. 'cnt')
    """

    #with open("../data/bike_sharing.csv") as myfile:
    df = pd.read_csv(file_path)

    X, y = df[x_var].values.tolist(), list(df["pc"]) 
 
    return X, y


def split_data_randomly(data, prob):
    """
    input:
    - data: a list of pairs of x,y values
    - prob: the fraction of the dataset that will be testing data, typically
    prob=0.2

    output:
    - a tuple of two lists with training data pairs and testing data pairs,
    respectively.
    """
    # input assumed to look like this: [ [[x1, x2, ...], y], [[x1, x2, ...], y], ... ]
    # placeholders - do not change this. first list: training data,
    # second list: testing data
    random.shuffle(data)
    train = data[:int(len(data) * (1-prob) + 1)]
    test = data[int(len(data) * (1-prob) + 1):]
   
    # TODO: Split data randomly into fractions [prob, 1 - prob]. populate the lists
    # in the tuple
    pass
    # return - you should not change this
    results = train, test
    return results


def train_test_split(x, y, test_pct=0.2):
    """
    input:
        x: list of x values
        y: list of independent values
        test_pct: percentage of the data that is testing data (0.2 by default).

    output: x_train, x_test, y_train, y_test lists
    """
    #x: [[x1,x2,...], [x1,x2,...], [x1,x2,...], .... ]
    #y: [y1, y2, .... ]
    # placeholders
    x_train, x_test, y_train, y_test = [], [], [], []

    data = []
    for i in range(len(x)):
        data.append((x[i], y[i]))

    train, test = split_data_randomly(data, test_pct)

    for i in range(len(train)):
        x_train.append(train[i][0])
        y_train.append(train[i][1])

    for i in range(len(test)):
        x_test.append(test[i][0])
        y_test.append(test[i][1])

    # TODO: Split the features X and the labels y into x_train, x_test and
    # y_train, y_test as specified by test_pct. You may want to use split_data_randomly
    # in this function
    pass
    # and then return :)
    return x_train, x_test, y_train, y_test


def calculate_r_squared(y_test, y_predicted):
    """
    Calculate the r-squared value

    Note: use the funciont R-Squared = 1 - SSE/SSTO

    input:
        y_test (list): the actual y values
        y_predicted (list): the predicted y values from the model

    output:
        r-squared (float)
    """
    sse = 0
    ssto = 0

    mean = sum(y_test) / len(y_test)

    for i in range(len(y_test)):
        sse += (y_test[i] - y_predicted[i])**2
        ssto += (y_test[i] - mean)**2
        
    r_squared_value = 1 - (sse/ssto) # placeholder

    return r_squared_value
