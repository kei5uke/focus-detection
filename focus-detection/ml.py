from hyperopt import Trials, STATUS_OK, tpe
from hyperas import optim
from hyperas.distributions import choice

from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, LSTM

import pandas as pd
import numpy as np
import collections

import gc
from tensorflow.python.keras import backend as K
K.clear_session()
gc.collect()


def model(x_train, y_train):
    model = Sequential()
    model.add(Dense(x_train.shape[1],
                   input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout({{uniform(0, 0.5)}}))
    model.add(LSTM(16,
                   return_sequences=False))
    model.add(Dropout({{uniform(0, 0.5)}}))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss = 'binary_crossentropy',
                  optimizer = 'adam',
                  metrics = ['acc'])

    history = model.fit(x_train,
              y_train,
              epochs = {{choice([16, 32 ,64])}},
              batch_size = {{choice([32 ,64 ,128])}},
              validation_split = 0.1,
              shuffle = False)

    val_acc = np.amax(history.history['val_acc'])
    print(f'Best epoch acc:{val_acc}')

    return {'loss': -val_acc, 'status': STATUS_OK, 'model': model}

def data():
    df = pd.read_csv('../csv/tmp.csv', header=0)
    data = df[(df['STATE'] >= 2) & (df['STATE'] <= 5)]
    X = data[['GSR', 'Delta', 'Theta', 'Low_Alpha', 'High_Alpha', 'Low_Beta', 'High_Beta', 'Low_Gamma', 'Mid_Gamma']].values
    mean = X.mean(axis = 0)
    std = X.std(axis = 0)

    # Train data
    data = df[(df['STATE'] >= 2) & (df['STATE'] <= 3)]
    X = data[['GSR', 'Delta', 'Theta', 'Low_Alpha', 'High_Alpha', 'Low_Beta', 'High_Beta', 'Low_Gamma', 'Mid_Gamma']].values
    X = (X - mean) / std
    y = data['STATE']
    x_train, y_train = create_data(X, y)

    # Test data
    data = df[(df['STATE'] >= 4) & (df['STATE'] <= 5)]
    X = data[['GSR', 'Delta', 'Theta', 'Low_Alpha', 'High_Alpha', 'Low_Beta', 'High_Beta', 'Low_Gamma', 'Mid_Gamma']].values
    X = (X - mean) / std
    y = data['STATE']
    x_test, y_test = create_data(X, y)

    return x_train, y_train, x_test, y_test, mean, std

def create_data(X, y):
    time_step=30;
    x_data, y_data = [], []

    for i in range(0, len(X) -time_step, 1):
        #x_data
        tmp = X[i:(i+time_step)].tolist()
        x_data.append(tmp)
        #y_data
        labels = y[i:(i+time_step)]
        mode = collections.Counter(labels).most_common()[0][0]
        if mode % 2 == 0:
            y_data.append(1)
        if mode % 2 == 1:
            y_data.append(0)

    return np.array(x_data), np.array(y_data).reshape(-1,1)

def auto_tuning(filename: str):
    best_run, best_model = optim.minimize(model=model,
                                      data=data,
                                      algo=tpe.suggest,
                                      max_evals=3,
                                      eval_space=True,
                                      trials=Trials(),
                                      functions=[create_data])

    x_train, y_train, x_test, y_test, mean, std = data()
    test_loss, test_acc = best_model.evaluate(x_test, y_test)
    print(f'Test loss:{test_loss}, Test acc:{test_acc}')
    print(f'Best Run:{best_run}')

    best_model.save('../keras_model/' + filename)

    return best_model, mean, std


if __name__ == '__main__':
    auto_tuning('test')
