import numpy as np
import tensorflow as tf
import pickle

class ClassificationModelUsage:
    def __init__(self):
        self.loaded_model = tf.keras.models.load_model('text_classifier.keras')
        with open('label_encoder.pkl', 'rb') as f:
            self.loaded_encoder = pickle.load(f)
    def predict(self, text):
        input_data = tf.convert_to_tensor([text], dtype=tf.string)
        probas = self.loaded_model.predict(input_data)
        predicted_idx = np.argmax(probas)
        return self.loaded_encoder.inverse_transform([predicted_idx])[0]


if __name__ == "__main__":
    CMusage = ClassificationModelUsage()
    print(CMusage.predict("Не горит лампа в коридоре"))