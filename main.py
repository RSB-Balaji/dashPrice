import numpy as np
import pandas as pd
import evaluation as eval
from sklearn.svm import SVC

def Load_data():
    train = pd.read_csv('train_set.csv')
    test = pd.read_csv('test_set.csv')
    return train, test

class SVMModel():
    def __init__(self, n):
        self.model = SVC(kernel = 'poly', degree = 3) 
    
    def train(self, X, Y):
        self.model.fit(X, Y)

    def predict(self, X):
        return np.array(self.model.predict(X))


def main():
    features = [
        'EMA10','EMA12','EMA20','EMA26','EMA50','EMA100','EMA200',
        'SMA5','SMA10','SMA15','SMA20','SMA50','SMA100','SMA200',]
    label = ['Class']

    df_train, df_test = Load_data()
    Xtrain = df_train[features].values
    Ytrain = df_train[label].values.ravel()
    Xtest = df_test[features].values
    Ytest = df_test[label].values.ravel()

    svm_poly = SVMModel(2)
    svm_poly.train(Xtrain, Ytrain)
    Ypredicted = np.array(svm_poly.predict(Xtest))
    print(eval.accuracy(prediction = Ypredicted, true_class = Ytest))
    print(Ypredicted)

if __name__ == "__main__":
    main()
