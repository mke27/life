import numpy as np
import pandas as pd

df = pd.read_csv('datasets/preprocessed-datasets/alldata_unstandard.csv')

def my_pca(X):
    '''
        a function that performs PCA

        args:
            X: a n by d numpy array
        returns:
            Xhat: a n by p numpy array where p <= d
    '''

    # center X
    X_center = X - np.mean(X, axis=0)

    # covariance matrix of X
    Sigma = np.cov(X_center.T)

    # get the eigenvalues and eigenvectors
    evals, evecs = np.linalg.eig(Sigma)
 
    # print the eigenvalues and ask how many PCs to keep
    print(evals.round())
    print("\nHow many principal components to keep?:\n")
    k = int(input())

    # use the example code below and find the k largest eigenvalues
    # Get the indices of the k largest values
    indices = np.argsort(evals)[-k:]
    # Reverse to get them in descending order
    largest_indices = indices[::-1]
    
    # and find v, the matrix with the largest eigenvectors
    evec = evecs[:,largest_indices]

    # make Xhat by taking the centered X and multiplying v
    Xhat = X_center.dot(evec)
    
    # remove the pass and replace with return Xhat
    return Xhat

X = df[['healthcare', 'education', 'safety', 'environment', 'qol']].to_numpy()

Xhat = my_pca(X)

print(Xhat)