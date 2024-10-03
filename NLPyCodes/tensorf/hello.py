import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

# 상수 정의
a = 1.0
b = 1.0

# g(x)와 f(x) 모델을 Keras 레이어로 구현
class GModel(layers.Layer):
    def call(self, inputs):
        return a * tf.square(inputs) + b

class FModel(layers.Layer):
    def call(self, inputs):
        return tf.cos(a * inputs) + b

# 전체 모델 구성
input_dim = 1
inputs = layers.Input(shape=(input_dim,))
g_output = GModel()(inputs)
f_output = FModel()(g_output)

# 최종 모델 생성
final_model = keras.Model(inputs=inputs, outputs=f_output)

# 모델 컴파일
final_model.compile(optimizer='adam', loss='mean_squared_error')

# 데이터 생성
X_train = np.linspace(-10, 10, 100).reshape(-1, 1)
y_train = final_model.predict(X_train)

# 모델 훈련
final_model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

final_model.save('hello.h5')

# 모델 평가 및 예측
loss = final_model.evaluate(X_train, y_train)
X_new = np.array([[0], [1], [2]])
predictions = final_model.predict(X_new)

print("Predictions: ", predictions)
