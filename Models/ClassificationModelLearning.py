import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Параметры
VOCAB_SIZE = 10000
MAX_SEQUENCE_LENGTH = 200
EMBEDDING_DIM = 128
if __name__ == '__main__':
    # Загрузка данных
    df = pd.read_excel('L_proceed.xlsx')
    df['A'] = df['A'].fillna('')
    df['B'] = df['B'].fillna('')

    texts = df['A'].astype(str).values
    labels = df['B'].astype(str).values

    # Кодирование меток
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)
    num_classes = len(label_encoder.classes_)

    from sklearn.utils.class_weight import compute_class_weight
    class_weights = compute_class_weight('balanced', classes=np.unique(encoded_labels), y=encoded_labels)
    class_weight_dict = dict(enumerate(class_weights))

    import tensorflow as tf
    from tensorflow.keras.layers import TextVectorization



    # Векторизация текста
    vectorizer = TextVectorization(
        max_tokens=VOCAB_SIZE,
        output_mode='int',
        output_sequence_length=MAX_SEQUENCE_LENGTH)
    vectorizer.adapt(texts)

    # Модель
    model = tf.keras.Sequential([
        tf.keras.Input(shape=(1,), dtype=tf.string),
        vectorizer,
        tf.keras.layers.Embedding(VOCAB_SIZE, EMBEDDING_DIM),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
        tf.keras.layers.Dense(64, activation='relu', kernel_regularizer='l2'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])

    # Компиляция с учетом весов классов
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'],
        weighted_metrics=['accuracy'])

    X_train, X_val, y_train, y_val = train_test_split(texts, encoded_labels, test_size=0.2)

    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=5,
        batch_size=32,
        class_weight=class_weight_dict)

    import pickle
    print(model.summary())
    # Сохранение
    model.save('text_classifier.keras')

    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)