# -*- coding: utf-8 -*-
"""TensorBoard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MusdeWLUUKNy0pXqRwQwPh0gUgUzqkZQ

# **TensorBoard**

**Setup**
"""

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard

"""**Membuat File Log**"""

import datetime
import tensorflow as tf
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

!rm -rf ./logs/
tf.summary.create_file_writer("./logs/")

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

mnist = tf.keras.datasets.mnist
(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
def create_model():
  return tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
  ])
model = create_model()
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(x_train, y_train, epochs = 10,
    validation_data=(x_test, y_test),
    callbacks=[tensorboard_callback])

"""**TensorBoard Lokal**"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorboard --logdir logs/fit

"""**Tensorboard.dev**"""

!tensorboard dev upload --logdir logs/fit

"""**Menampilkan Gambar**"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

file_writer = tf.summary.create_file_writer(log_dir)
with file_writer.as_default():
    img = np.reshape(x_train[0], (-1, 28, 28, 1))
    tf.summary.image('Training Data ', img, step = 0)
# %tensorboard --logdir logs/fit

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

file_writer = tf.summary.create_file_writer(log_dir)
with file_writer.as_default():
  imgs = np.reshape(x_train[0:4], (-1, 28, 28, 1))
  tf.summary.image('4 Training Data ', imgs, max_outputs = 4, step = 0)

# %tensorboard --logdir logs/fit

import io
import matplotlib.pyplot as plt

def plot_to_image(figure):
  """Ubah the matplotlib plot 'figure' ke PNG image"""
  # Simpan plot ke PNG di memori
  buf = io.BytesIO()
  plt.savefig(buf, format='png')
  # Tutup the figure untuk mencegah figure ditampilkan langsung di Notebook
  plt.close(figure)
  buf.seek(0)
  # Ubh PNG buffer ke TF image
  image = tf.image.decode_png(buf.getvalue(), channels=4)
  # Tambah dimensi
  image = tf.expand_dims(image, 0)
  return image

!rm -rf logs/plots

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
import datetime

logdir = "logs/plots/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
file_writer = tf.summary.create_file_writer(logdir)

class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def image_grid():
  """Return a 5x5 grid of the MNIST images as a matplotlib figure."""
  # Create a figure to contain the plot.
  figure = plt.figure(figsize=(10,10))
  for i in range(25):
    # Start next subplot.
    plt.subplot(5, 5, i + 1, title=class_names[y_train[i]])
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(x_train[i], cmap=plt.cm.binary)

  return figure

# Prepare the plot
figure = image_grid()
# Convert to image and log
with file_writer.as_default():
  tf.summary.image("Training data", plot_to_image(figure), step=0)

# %tensorboard --logdir logs/plots

"""**Confusion Matrix**"""

"""Pembuatan plot confusion matrix"""

def plot_confusion_matrix(cm, class_names):


  """ Mengembalikan matplotlib figure yang berisi the plot confusion matrix  """


  figure = plt.figure(figsize=(8, 8))
  plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
  plt.title("Confusion matrix")
  plt.colorbar()
  tick_marks = np.arange(len(class_names))
  plt.xticks(tick_marks, class_names, rotation=45)
  plt.yticks(tick_marks, class_names)


  # Normalisasi confusion matrix.
  cm = np.around(cm.astype('float') / cm.sum(axis=1)[:, np.newaxis], decimals=2)


  # Setting teks
  threshold = cm.max() / 2.
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    color = "white" if cm[i, j] > threshold else "black"
    plt.text(j, i, cm[i, j], horizontalalignment="center", color=color)


  plt.tight_layout()
  plt.ylabel('True label')
  plt.xlabel('Predicted label')
  return figure

"""Log matrix yang dibuat pada setiap epoch untuk men-generate sebuah confusion
matrix, kemudian mengubahnya menjadi PNG pada fungsi plot_to_image."""

import sklearn.metrics
import itertools

def log_confusion_matrix(epoch, logs):
  # Gunakan model untuk memprediksi nilai dari data validasi
  test_pred_raw = model.predict(x_test)
  test_pred = np.argmax(test_pred_raw, axis=1)

  # Hitung confusion matrix.
  cm = sklearn.metrics.confusion_matrix(y_test, test_pred)

  figure = plot_confusion_matrix(cm, class_names=class_names)
  cm_image = plot_to_image(figure)

  # Log confusion matrix sebagai image summary.
  with file_writer_cm.as_default():
    tf.summary.image("Confusion Matrix", cm_image, step=epoch)

# Definisikan epoch setiap callback
cm_callback = tf.keras.callbacks.LambdaCallback(on_epoch_end=log_confusion_matrix)

# Commented out IPython magic to ensure Python compatibility.
"""Pemanggilan multiple callbacks. Callback pertama digunakan untuk menyimpan log skalar,
log lainnya digunakan untuk plot confusion matrix. Callback kedua yaitu LambdaCallback digunakan
untuk mengeksekusi kode bebas."""
import datetime

logdir = "logs/image/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# Definisikan callback.
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)
file_writer_cm = tf.summary.create_file_writer(logdir + '/cm')


# Train the classifier.
model.fit(
    x_train, y_train, epochs=5,
    callbacks=[tensorboard_callback, cm_callback],
    validation_data=(x_test, y_test),
)

# Start TensorBoard.
# %tensorboard --logdir logs/image