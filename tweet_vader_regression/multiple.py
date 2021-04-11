import numpy as np
import random
import statsmodels.api as sm
from statsmodels.tools import eval_measures
from util import train_test_split, load_file, calculate_r_squared

def multiple_regression(X_train, X_test, y_train, y_test):
    """
    A multiple linear regression using StatsModel
    Inputs:
    - X_train, X_test, y_train, y_test: lists of training and testing values

    Outputs:
    - The Mean Squared Error value when applying the model on the training
    dataset (training_MSE)
    - The Mean Squared Error value when applying the model on the testing
    dataset (testing_MSE)
    - The R-Squared value when applying the model on the *training* dataset
    (training_R2)
    """
    # Placeholder - your function should update these three variables and
    # return the correct values for these three variables!
    training_MSE, testing_MSE, testing_R2 = 0, 0, 0

    # TODO: Use StatsModels to create the Linear Model and Output R-squared
    #X_train, X_test, y_train, y_test = np.array(X_train), np.array(X_test), np.array(y_train), np.array(y_test)
    
    X_train = sm.add_constant(X_train)
    model = sm.OLS(y_train, X_train)
    
    results = model.fit()
    # TODO: Prints out the Report
    print(results.summary())

    X_test = sm.add_constant(X_test)
    train_prediction = results.predict(X_train)
    print(results.mse_total)
    test_prediction = results.predict(X_test)
 
    
    training_MSE = eval_measures.mse(y_train, train_prediction )
    testing_MSE = eval_measures.mse(y_test, test_prediction)
    
    testing_R2 = calculate_r_squared(y_test, results.predict(X_test))


    # return
    return training_MSE, testing_MSE, testing_R2



if __name__=='__main__':

    # DO not change this seed. It guarantees that all students perform the same
    # train and test split
    random.seed(1)


    # TODO: Call load_file; x_var should be a list
    X, y = load_file('./sentiments.csv', ["comments","likes","pos","neg","neu","num_tweets"]) 
    X_train, X_test, y_train, y_test = train_test_split(X, y,0.5)

    # TODO: use train_test_split to split data into x_train, x_test, y_train,
    # y_test

    training_MSE, testing_MSE, testing_R2 = multiple_regression(X_train, X_test, y_train, y_test)

    print(training_MSE)
    print(testing_MSE)
    print(testing_R2)
    # TODO: Call multiple_regression
