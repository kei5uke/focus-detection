import pandas as pd
import numpy as np
from scipy import stats

from hyperopt import Trials, STATUS_OK, tpe
from hyperas import optim
from hyperas.distributions import choice

import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, LSTM


def create_data(X,Y):
    time_step=120
    x_data, y_data = [], []

    for i in range(0,X.size-time_step,1):
        #x_data
        tmp = X.iloc[i:(i+time_step)]
        x_data.append(tmp)
        #y_data
        labels = Y[i:(i+time_step)]
        mode = stats.mode(labels)[0][0]
        if mode == 2 or mode == 4:
            y_data.append(1)
        if mode == 3 or mode == 5:
            y_data.append(0)
        x = np.array(x_data)
        y = np.array(y_data).reshape(-1,1)
    return x.astype('float32'),y.astype('float32')

def mean_and_std(x):
    data = x.astype('float32')
    mean = data.mean(axis=0)
    data -= mean
    std = data.std(axis=0)
    return mean, std

def data():
    df = pd.read_csv('gsr_record.csv',header=0)
    df = df.set_index('STATE')
    df = df.drop([1])
    
    df_train = df.copy()
    df_train = df_train.drop([4,5])
    x_train, y_train = create_data(df_train['GSR'],df_train.index.to_list())
    
    df_test = df.copy()
    df_test = df_test.drop([2,3])
    x_test, y_test = create_data(df_test['GSR'],df_test.index.to_list())
    
    mean, std = mean_and_std(x_train[0])
    x_train -= mean
    x_train /= std
    
    mean, std = mean_and_std(x_test[0])
    x_test -= mean
    x_test /= std
    
    x_train = np.reshape(x_train,[x_train.shape[0],x_train.shape[1],1])
    x_test = np.reshape(x_test,[x_test.shape[0],x_test.shape[1],1])
    
    return x_train, y_train, x_test, y_test

def model(x_train, y_train, x_test, y_test):
    model = Sequential()
    model.add(LSTM({{choice([2,4,8])}}, input_shape=(x_train.shape[1],1),return_sequences=True))
    model.add(Dropout({{uniform(0,1)}}))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['acc'])
    model.fit(x_train,
              y_train,
              epochs={{choice([8,16,32])}},
              batch_size={{choice([16,32,64])}},
              validation_data=(x_test,y_test),
              shuffle=False)
    val_loss, val_acc = model.evaluate(x_test, y_test, verbose=0)
    return {'loss': -val_acc, 'status': STATUS_OK, 'model': model}

def auto_tuning():
    #Get best_model
    best_run, best_model = optim.minimize(model=model,
                                          data=data,
                                          algo=tpe.suggest,
                                          max_evals=2,
                                          trials=Trials(),
                                          functions=[create_data,mean_and_std])
    #Get mean and std
    df = pd.read_csv('gsr_record.csv',header=0)
    df = df.set_index('STATE')
    df = df.drop([1,2,3])
    x, y = create_data(df['GSR'],df.index.to_list())
    mean, std = mean_and_std(x[0])

    #Model summary
    x_train, y_train, x_test, y_test = data()
    val_loss, val_acc = best_model.evaluate(x_test, y_test)
    print(best_model.summary())
    print("val_loss:",val_loss)
    print("val_acc:",val_acc)

    return best_model, mean, std
