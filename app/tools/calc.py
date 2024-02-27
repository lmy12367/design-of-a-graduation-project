import tensorflow as tf
import keras
import numpy as np
from sklearn import preprocessing
import pandas as pd

def run_calc(path,data_list) :
    data1 = np.loadtxt(open(path, 'rb'), delimiter=",", skiprows=1)
    x_train = data1[:, 0:6]   # 二维数据
    y = data1[:, 6:12]     # 二维数据

    # 将y数据进行归一化处理
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1))   # 默认范围为0-1
    y_train = min_max_scaler.fit_transform(y)

    print('x_train:', x_train)
    print('y_train:', y_train)

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(15, input_dim=6, activation="tanh", use_bias=True))   # 搭建5层隐藏层的BP神经网络
    model.add(tf.keras.layers.Dense(20, input_dim=15, activation="tanh", use_bias=True))
    model.add(tf.keras.layers.Dense(20, input_dim=20, activation="tanh", use_bias=True))
    model.add(tf.keras.layers.Dense(30, input_dim=20, activation="tanh", use_bias=True))
    model.add(tf.keras.layers.Dense(25, input_dim=30, activation="tanh", use_bias=True))
    model.add(tf.keras.layers.Dense(6, input_dim=25, activation="tanh", use_bias=True))

    model.compile(loss="mean_squared_error", optimizer="Adam")        # 配置神经网络的损失函数和优化器   loss="mean_squared_error"

    model.fit(x_train, y_train, epochs=20000, verbose=1)               # 代入输入值和输出值进行训练神经网络

    model.save_weights("./modelWeights.h5")                        # 将训练后的权重值进行保存，方便后续调用预测

    predictResult1 = model.predict(np.array(data_list).reshape(1, 6))
    predictResult = min_max_scaler.inverse_transform(predictResult1)
    return predictResult.tolist()[0]

if __name__ == "__main__" :
    file_path = r"C:\Users\ty\Desktop\界面接口程序 - 4.4\1数据\1万\1万横低满.csv"
    data_list = [0.8, 8, 8.3, 9.2, 12.01, 7.14]

    res = run_calc(file_path,data_list)
    print("res: ", res)