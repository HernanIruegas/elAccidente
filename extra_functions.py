"""
    --------------
        K-MEANS
    --------------

    Task
    -----
    Find the mean value of each indicated subset

    Parameters
    ----------
    list    : list or matrix
                Values to group
    cluster : int, by defult 2
                Indicates the subsets

    Returns
    ----------
    array with indicator where that elem belongs
    nice-to-have : crosstab, Dataframe.

    Comments
    --------

    Examples
    --------
    input list example
    >>> list = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
    >>> list = [[1, 1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,7], [8,8], [9,9], [10,10]]

    into numpy array
    a = [1, 2, 3, 4, 5, 6] >> a = [1 2 3 4 5 6]

    A = [[1, 2, 3],        >> A = [[1 2 3],
        [4, 5, 6]]                [4 5 6]]
"""
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

def k_means(k_list, cluster=2):

    # convert into numpy array-format to manipulate it
    x = np.array(k_list)

    # does the clasification of the elemens given the clusters
    # models the data into the kmeans model
    kmeans = KMeans(n_clusters=cluster).fit(x)

    # display the clusters and the clasification
    print("\ncluster_centers_")
    print(kmeans.cluster_centers_)

    print("\nkmeans.labels_")
    km = kmeans.labels_
    print(km)
    # return(km)


"""
    -----------------------
        LINEAR-REGRESSION
    -----------------------

    Task
    -----
    Predicts a value given a linear model

    Parameters
    ----------
    matrix    : matrix, 2-D array
    predict   : number

    Returns
    ----------
    array with indicator where that elem belongs

    Comments
    --------
    It would be nice if the user can user an array of values to be predicted

    Examples
    --------
    input matrix example
    >>> m = [[1, 1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,7], [8,8], [9,9], [10,10]]
"""
from sklearn.linear_model import LinearRegression
import numpy as np

def linear_regression(matrix, predict)
    # convert the matrix into numpy array in order to get the values
    n_matrix = np.array(matrix[0:], dtype = np.int16)

    # store the values of the rows and columns
    a_x = n_matrix[0:,0]
    a_y = n_matrix[0:,1]

    # reshape the arrays to calculate the linear model
    m_x = np.reshape(a_x, (-1, 1))
    m_y = np.reshape(a_y, (-1, 1))

    # set the data into lineal modelRidge
    lineal = LinearRegression().fit(m_x, m_y)

    print("\n Prediction")
    # here comes the input given
    fp = lineal.predict(np.reshape(predict,(1,-1)))
    print(fp)
    # return(fp)


"""
    ----------------------
        RIDGE-REGRESSION
    ----------------------

    Task
    -----
    Predicts a value given a linear model

    Parameters
    ----------
    matrix    : matrix, 2-D array
    alpha     : positive float, corresponds to C^-1

    Returns
    ----------
    array     : Σ_interception_coefitient

    Comments
    --------

    Examples
    --------
    input matrix example
    >>> matrix = [[11, 3], [2, 2], [37, 3], [4, 444], [5, 5], [99, 6], [7, 75], [8, 18], [9, 9], [134, 10],
            [2, 31], [78, -55], [62, 1], [90, -99], [34, 91], [22, 66], [923, -761], [768, 7761], [2, 77]]
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

def ridge(matrix, alpha):

    n_matrix = np.array(matrix[0:], dtype = np.int16)
    x = n_matrix[0:,0]
    y = n_matrix[0:,1]

    #  Format the data
    data = pd.DataFrame(np.column_stack([x,y]),columns=['x','y'])
    for i in range(2,16):
        colname = 'x_%d'%i
        data[colname] = data['x']**i

    # Initialize predictors:
    predictors=['x']

    # Fit the model
    ridgereg = Ridge(alpha = alpha, normalize=True)
    ridgereg.fit(data[predictors],data['y'])
    y_pred = ridgereg.predict(data[predictors])

    # Return the result in pre-defined format
    rss = sum((y_pred-data['y'])**2)

    # add interception and coefitient
    ret = [rss]
    ret.extend([ridgereg.intercept_])
    ret.extend(ridgereg.coef_)

    print("\n Ridge\nΣ_interception_coefitient")
    print(ret)
    # return(ret)

"""
    ----------------------
        LASSO-REGRESSION
    ----------------------

    Task
    -----
    Predicts a value given a linear model

    Parameters
    ----------
    matrix    : matrix, 2-D array

    Returns
    ----------
    array     : Σ_interception_coefitient

    Comments
    --------

    Examples
    --------
    input matrix example
    >>> matrix = [[11, 3], [2, 2], [37, 3], [4, 444], [5, 5], [99, 6], [7, 75], [8, 18], [9, 9], [134, 10],
            [2, 31], [78, -55], [62, 1], [90, -99], [34, 91], [22, 66], [923, -761], [768, 7761], [2, 77]]
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso

def lasso(matrix):

    n_matrix = np.array(matrix[0:])
    x = n_matrix[0:,0]
    y = n_matrix[0:,1]

    #  Format the data
    data = pd.DataFrame(np.column_stack([x,y]),columns=['x','y'])
    for i in range(2,16):
        colname = 'x_%d'%i
        data[colname] = data['x']**i

    # Initialize predictors:
    predictors=['x']

    # Fit the model
    lassoreg = Lasso(normalize=True)
    lassoreg.fit(data[predictors],data['y'])
    y_pred = lassoreg.predict(data[predictors])

    # Return the result in pre-defined format
    rss = sum((y_pred-data['y'])**2)

    # add interception and coefitient
    ret = [rss]
    ret.extend([lassoreg.intercept_])
    ret.extend(lassoreg.coef_)

    print("\n Lasso Regression\nΣ_interception_coefitient")
    print(ret)
    # return(ret)

"""
    ----------------------
        TIME SERIES SPLIT
    ----------------------

    Task
    -----
    Provides train/test indices to split time series data samples that are observed
    at fixed time intervals, in train/test sets.
    In each split, test indices must be higher than before,
    and thus shuffling in cross validator is inappropriate.

    Parameters
    ----------
    matrix    : int
    array     : int, lenth of matrix
    splits    : int, number of splits

    Returns
    ----------
    void     : split time

    Comments
    --------

    Examples
    --------
    input matrix example
    >>> matrix = [[1, 2], [3, 4], [1, 2], [3, 4], [1, 2], [3, 4]]
    >>> array = [1, 2, 3, 4, 5, 6]
"""
from sklearn.model_selection import TimeSeriesSplit
import numpy as np

def time_series_split(matrix, array, splits);
    # convert into the format required
    X = np.array(matrix)
    y = np.array(array)

    # calculate the splits
    tscv = TimeSeriesSplit(n_splits=splits)

    # display
    # for train_index, test_index in tscv.split(X):
    #     print("TRAIN:", train_index, "TEST:", test_index)
    #     X_train, X_test = X[train_index], X[test_index]
    #     y_train, y_test = y[train_index], y[test_index]
    print("Time Series Split")
    return("this…")


"""
    ----------------------
        Mini Batch Means
    ----------------------

    Task
    -----


    Parameters
    ----------
    matrix    :  float array 2-D

    cluster : int, by defult 3
                Indicates the subsets

    Returns
    ----------
    array with indicator where that elem belongs
    nice-to-have : crosstab, Dataframe.

    Comments
    --------

    Examples
    --------
    input list example
    >>> list = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
    >>> list = [[1, 1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,7], [8,8], [9,9], [10,10]]
"""

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import MiniBatchKMeans
import numpy as np

def miniBatch(matrix, cluster=8):

    # convert into numpy array in order to get the index
    x = np.array(matrix)

    # Standardize features by removing the mean and scaling to unit variance
    scaler = StandardScaler()
    X_std = scaler.fit_transform(x)

    # Create k-mean object
    clustering = MiniBatchKMeans(n_clusters=cluster, batch_size=100)

    # Train model
    mini = clustering.fit(X_std)

    # display
    print(mini.labels_)
    # return(mini.labels_)

"""
    ------------------------
        Mean Squared Error
    ------------------------

    Task
    -----


    Parameters
    ----------
    a1      : int, float. Array
    a1      : int, float. Array

    OR
    m1      : int, float. Matrix
    m1      : int, float. Matrix

    Returns
    ----------
    float, error.

    Comments
    --------

    Examples
    --------
    input list example
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]

    input list example
    y_true = [[0.5, 1],[-1, 1],[7, -6]]
    y_pred = [[0, 2],[-1, 2],[8, -5]]
"""
def mean_sqrt_error(y_true, y_pred):
    print("\n\t Mean Squared Error")
    mse = mean_squared_error(y_true, y_pred)
    print(mse)
    # return(mse)

"""
    ------------------------
        Mean Absolute Error
    ------------------------

    Task
    -----


    Parameters
    ----------
    a1      : int, float. Array
    a1      : int, float. Array

    OR
    m1      : int, float. Matrix
    m1      : int, float. Matrix

    Returns
    ----------
    float, error.

    Comments
    --------

    Examples
    --------
    input list example
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]

    input matrix example
    y_true = [[0.5, 1],[-1, 1],[7, -6]]
    y_pred = [[0, 2],[-1, 2],[8, -5]]
"""
def mean_abs_error(y_true, y_pred):
    print("\n\t Mean Absolute Error")
    mae = mean_absolute_error(y_true, y_pred)
    print(mae)
    # return(mean_absolute_error)

"""
    ------------------------
        Median Absolute Error
    ------------------------

    Task
    -----


    Parameters
    ----------
    a1      : int, float. Array
    a1      : int, float. Array

    Returns
    ----------
    float, error.

    Comments
    --------

    Examples
    --------
    input list example
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
"""
def median_abs_error(y_true, y_pred):
    print("\n\t Median Array")
    mae = median_absolute_error(y_true, y_pred)
    print(mae)
    # return(mae)


import scipy.stats as stats
import statistics as st
import numpy as np

"""
    -----------
        Mean 
    -----------
      
    Task
    -----
    calculates an average from a population or sample

    Parameters 
    ----------
    a1      : int, float. 1-D List

    Returns 
    ----------
    float

    Comments
    --------
    leads to error if data is empty, or not numbers

    Examples
    --------
    input list example
    a1 = [9,8,7,6,5,4,3,666,2,1,2,3,3,4,4,4,5,5,5,5,5,5,5,5,666,99,221,11,54,36]

"""


def mean(a1):
    # return(st.mean(a1))


"""
    -------------
        Median 
    -------------
      
    Task
    -----
    calculates the middle value of data

    Parameters 
    ----------
    a1      : int, float. 1-D List

    Returns 
    ----------
    float 

    Comments
    --------
    leads to error if data is empty

    Examples
    --------
    input list example
    a1 = [9,8,7,6,5,4,3,666,2,1,2,3,3,4,4,4,5,5,5,5,5,5,5,5,666,99,221,11,54,36]

"""
def median(a1):
    # return(st.mean(a1))


"""
    --------------
        Median 
    --------------
      
    Task
    -----
    calculates the most common value of discrete value

    Parameters 
    ----------
    a1      : int, float. 1-D List

    Returns 
    ----------
    int, float, depends of the given set

    Comments
    --------
    leads to error if data is empty, or if there is not exactly one most common value
    leads to error if data is not discrete

    Examples
    --------
    input list example
    a1 = [9,8,7,6,5,4,3,666,2,1,2,3,3,4,4,4,5,5,5,5,5,5,5,5,666,99,221,11,54,36]

"""
def mode(a1):
    # return(st.mode(a1))


"""
    -------------------------
        Standard Deviation 
    -------------------------
      
    Task
    -----
    samples the standard deviation of data

    Parameters 
    ----------
    a1      : int, float. 1-D List

    Returns 
    ----------
    float

    Comments
    --------
    leads to error if data is empty
    leads to error if data has not numeric values

    Examples
    --------
    input list example
    a1 = [9,8,7,6,5,4,3,666,2,1,2,3,3,4,4,4,5,5,5,5,5,5,5,5,666,99,221,11,54,36]

"""
def stddev(a1):
    # return(st.stdev(a1))


"""
    ---------------
        Variance
    ---------------
      
    Task
    -----
    samples the variance of data

    Parameters 
    ----------
    a1      : int, float. 1-D List

    Returns 
    ----------
    float

    Comments
    --------
    leads to error if data is empty
    leads to error if data has not numeric values

    Examples
    --------
    input list example
    a1 = [9,8,7,6,5,4,3,666,2,1,2,3,3,4,4,4,5,5,5,5,5,5,5,5,666,99,221,11,54,36]

"""
def variance(a1):
    # return(st.variance(a1))


"""
    ---------------
        SKEWNESS
    ---------------
      
    Task
    -----
    samples the variance of data

    Parameters 
    ----------
    a1      : int, float. 1-D List

    Returns 
    ----------
    float

    Comments
    --------
    leads to error if data is empty
    leads to error if data has not numeric values

    Examples
    --------
    input list example
    a1 = [9,8,7,6,5,4,3,666,2,1,2,3,3,4,4,4,5,5,5,5,5,5,5,5,666,99,221,11,54,36]

"""
def skew(a1):
    x = np.array(a1)
    sk = stats.skew(x)
    # return(st.skew(sk))


"""
    ---------------
        KURTOSIS
    ---------------
      
    Task
    -----
    samples the variance of data

    Parameters 
    ----------
    a1      : int, float. 1-D List

    Returns 
    ----------
    float

    Comments
    --------
    leads to error if data is empty
    leads to error if data has not numeric values

    Examples
    --------
    input list example
    a1 = [9,8,7,6,5,4,3,666,2,1,2,3,3,4,4,4,5,5,5,5,5,5,5,5,666,99,221,11,54,36]

"""
def kurt(a1):
    x = np.array(a1)
    kr = stats.skew(x)
    # return(st.skew(kr))


"""
    -----------------
        FREQUENCY
    -----------------
      
    Task
    -----
    counts the times an element was fount on a set

    Parameters 
    ----------
    a1      : int, float. 1-D List

    Returns 
    ----------
    1-D array

    Comments
    --------
    leads to error if data is empty
    leads to error if data has not numeric values

    Examples
    --------
    input list example
    a1 = [9,8,7,6,5,4,3,666,2,1,2,3,3,4,4,4,5,5,5,5,5,5,5,5,666,99,221,11,54,36]

"""
def freq(a1):
    unique_elements, counts_elements = np.unique(a1, return_counts=True)
    f = np.column_stack([unique_elements,counts_elements])
    # return(f)

