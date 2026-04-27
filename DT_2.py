import numpy as np 
import pandas as pd 
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
       		 print(os.path.join(dirname, filename))
import numpy as np
import pandas as pd
import os
from pathlib import Path
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

print(tf.__version__)


train_dir = Path(r'C:\Users\mas_r\OneDrive\Desktop\Major project\Dataset\train')
train_filepaths = list(train_dir.glob(r'**/*.jpg'))

test_dir = Path(r'C:\Users\mas_r\OneDrive\Desktop\Major project\Dataset\test')
test_filepaths = list(test_dir.glob(r'**/*.jpg'))

val_dir = Path(r'C:\Users\mas_r\OneDrive\Desktop\Major project\Dataset\validation')
val_filepaths = list(val_dir.glob(r'**/*.jpg'))




def image_processing(filepath):
    """Create a DataFrame with the filepath and the labels of the pictures."""
    labels = [Path(fp).parts[-2] for fp in filepath]
    filepath_series = pd.Series(filepath, name='Filepath').astype(str)
    labels_series = pd.Series(labels, name='Label')
    df = pd.concat([filepath_series, labels_series], axis=1).sample(frac=1).reset_index(drop=True)
    return df

# Process the filepaths for train, test, and validation sets
train_df = image_processing(train_filepaths)
test_df = image_processing(test_filepaths)
val_df = image_processing(val_filepaths)



# Data Generators
train_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input,
    rotation_range=30,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    horizontal_flip=True,
    fill_mode="nearest"
)
val_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
)

train_images = train_generator.flow_from_dataframe(
    dataframe=train_df,
    x_col='Filepath',
    y_col='Label',
    target_size=(224, 224),
    class_mode='categorical',
    batch_size=32,
    shuffle=True,
    seed=0
)

val_images = val_generator.flow_from_dataframe(
    dataframe=val_df,
    x_col='Filepath',
    y_col='Label',
    target_size=(224, 224),
    class_mode='categorical',
    batch_size=32,
    shuffle=True,
    seed=0
)





# Define MobileNetV2 model
mobilenet_base = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet',
    pooling='avg'
)
mobilenet_base.trainable = False

inputs_mobilenet = mobilenet_base.input
x_mobilenet = tf.keras.layers.Dense(128, activation='relu')(mobilenet_base.output)
x_mobilenet = tf.keras.layers.Dense(128, activation='relu')(x_mobilenet)
outputs_mobilenet = tf.keras.layers.Dense(len(train_df.Label.unique()), activation='softmax')(x_mobilenet)

model_mobilenet = tf.keras.Model(inputs=inputs_mobilenet, outputs=outputs_mobilenet)

model_mobilenet.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
# Define VGG16 model
vgg_base = tf.keras.applications.VGG16(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet',
    pooling='avg'
)
vgg_base.trainable = False

inputs_vgg = vgg_base.input
x_vgg = tf.keras.layers.Dense(128, activation='relu')(vgg_base.output)
x_vgg = tf.keras.layers.Dense(128, activation='relu')(x_vgg)
outputs_vgg = tf.keras.layers.Dense(len(train_df.Label.unique()), activation='softmax')(x_vgg)

model_vgg = tf.keras.Model(inputs=inputs_vgg, outputs=outputs_vgg)

model_vgg.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)




inputs = tf.keras.Input(shape=(224, 224, 3))

# Feature Extraction
vgg_features = vgg16_model(inputs)
mobilenet_features = mobilenet_model(inputs)

# Combine Features
combined_features = tf.keras.layers.Concatenate()([vgg_features, mobilenet_features])

# Fully Connected Layers
x = tf.keras.layers.Dense(256, activation='relu')(combined_features)
x = tf.keras.layers.Dropout(0.5)(x)
outputs = tf.keras.layers.Dense(len(train_df.Label.unique()), activation='softmax')(x)

# Model
model = tf.keras.Model(inputs=inputs, outputs=outputs)

# Compile Model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)





# Train Model
history = model.fit(
    train_images,
    validation_data=val_images,
    epochs=5,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=2,
            restore_best_weights=True
        )
    ]
)

# Test Data Generator
test_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
)

test_images = test_generator.flow_from_dataframe(
    dataframe=test_df,
    x_col='Filepath',
    y_col='Label',
    target_size=(224, 224),
    class_mode='categorical',
    shuffle=False
)





pred = model.predict(test_images)
pred = np.argmax(pred, axis=1)

# Map Labels
labels = (train_images.class_indices)
labels = dict((v, k) for k, v in labels.items())
predicted_labels = [labels[k] for k in pred]

# Function for Single Image Prediction
def predict_single_image(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img = img_to_array(img)
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions, axis=-1)
    return labels[predicted_class[0]]

# Test Prediction on a Single Image
img_result = predict_single_image(r"C:\Users\mas_r\OneDrive\Desktop\Major project\Dataset\test\cabbage\Image_1.jpg")
print(img_result)

# Save Model
model.save('combined_model.h5')




# Import necessary libraries
import matplotlib.pyplot as plt

# Function to plot accuracy and loss for comparison
def plot_comparison(history1, history2, model_names):
    # Extract metrics
    acc1 = history1.history['accuracy']
    val_acc1 = history1.history['val_accuracy']
    loss1 = history1.history['loss']
    val_loss1 = history1.history['val_loss']

    acc2 = history2.history['accuracy']
    val_acc2 = history2.history['val_accuracy']
    loss2 = history2.history['loss']
    val_loss2 = history2.history['val_loss']

    epochs = range(1, len(acc1) + 1)

    # Plot accuracy comparison
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc1, 'r-', label=f'{model_names[0]} Train Acc')
    plt.plot(epochs, val_acc1, 'r--', label=f'{model_names[0]} Val Acc')
    plt.plot(epochs, acc2, 'b-', label=f'{model_names[1]} Train Acc')
    plt.plot(epochs, val_acc2, 'b--', label=f'{model_names[1]} Val Acc')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    # Plot loss comparison
    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss1, 'r-', label=f'{model_names[0]} Train Loss')
    plt.plot(epochs, val_loss1, 'r--', label=f'{model_names[0]} Val Loss')
    plt.plot(epochs, loss2, 'b-', label=f'{model_names[1]} Train Loss')
    plt.plot(epochs, val_loss2, 'b--', label=f'{model_names[1]} Val Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Train MobileNetV2
history_mobilenet = model_mobilenet.fit(
    train_images,
    validation_data=val_images,
    epochs=5,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=2,
            restore_best_weights=True
        )
    ]
)

# Train VGG16
history_vgg = model_vgg.fit(
    train_images,
    validation_data=val_images,
    epochs=5,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=2,
            restore_best_weights=True
        )
    ]
)

# Plot comparison of MobileNetV2 and VGG16
plot_comparison(history_mobilenet, history_vgg, ["MobileNetV2", "VGG16"])

