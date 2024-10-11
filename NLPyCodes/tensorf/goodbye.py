import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

a = 1.0
b = 1.0

# g(x)와 f(x) 모델을 Keras 레이어로 구현 (다시 정의)
class GModel(layers.Layer):
    def call(self, inputs):
        return a * tf.square(inputs) + b

class FModel(layers.Layer):
    def call(self, inputs):
        return tf.cos(a * inputs) + b

# 모델 로드
loaded_model = keras.models.load_model('hello.h5', custom_objects={'GModel': GModel, 'FModel': FModel})

# 새로운 입력 데이터
X_new = np.array([[10], [20], [30]])

# 로드한 모델로 예측하기
predictions_loaded = loaded_model.predict(X_new)
print("Loaded Model Predictions: ", predictions_loaded)
