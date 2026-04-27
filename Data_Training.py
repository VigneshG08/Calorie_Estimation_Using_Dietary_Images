# import numpy as np
# import pandas as pd
# import os
# from pathlib import Path
# import matplotlib.pyplot as plt
# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import load_img, img_to_array

# print(tf.__version__)

# # Define directories using raw strings to avoid escape character issues
# train_dir = Path(r'C:\Users\mas_r\OneDrive\Desktop\Major project\Dataset\train')
# train_filepaths = list(train_dir.glob(r'**/*.jpg'))

# test_dir = Path(r'C:\Users\mas_r\OneDrive\Desktop\Major project\Dataset\test')
# test_filepaths = list(test_dir.glob(r'**/*.jpg'))

# val_dir = Path(r'C:\Users\mas_r\OneDrive\Desktop\Major project\Dataset\validation')
# val_filepaths = list(val_dir.glob(r'**/*.jpg'))

# def image_processing(filepath):
#     """Create a DataFrame with the filepath and the labels of the pictures."""
    
#     # Extract labels using Path to handle file paths correctly
#     labels = [Path(fp).parts[-2] for fp in filepath]
    
#     # Create DataFrame from filepaths and labels
#     filepath_series = pd.Series(filepath, name='Filepath').astype(str)
#     labels_series = pd.Series(labels, name='Label')
    
#     # Combine into a DataFrame
#     df = pd.concat([filepath_series, labels_series], axis=1)
    
#     # Shuffle the DataFrame
#     df = df.sample(frac=1).reset_index(drop=True)
    
#     return df

# # Process the filepaths for train, test, and validation sets
# train_df = image_processing(train_filepaths)
# test_df = image_processing(test_filepaths)
# val_df = image_processing(val_filepaths)

# # Print some details about the training set
# print('-- Training set --\n')
# print(f'Number of pictures: {train_df.shape[0]}\n')
# print(f'Number of different labels: {len(train_df.Label.unique())}\n')
# print(f'Labels: {train_df.Label.unique()}')

# df_unique = train_df.copy().drop_duplicates(subset=["Label"]).reset_index()
# fig, axes = plt.subplots(nrows=6, ncols=6, figsize=(8, 7),
#                          subplot_kw={'xticks': [], 'yticks': []})
# for i, ax in enumerate(axes.flat):
#     ax.imshow(plt.imread(df_unique.Filepath[i]))
#     ax.set_title(df_unique.Label[i], fontsize=12)
# plt.tight_layout(pad=0.5)
# plt.show()

# train_generator = tf.keras.preprocessing.image.ImageDataGenerator(
#     preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
# )
# val_generator = tf.keras.preprocessing.image.ImageDataGenerator(
#     preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
# )

# train_images = train_generator.flow_from_dataframe(
#     dataframe=train_df,
#     x_col='Filepath',
#     y_col='Label',
#     target_size=(224, 224),
#     color_mode='rgb',
#     class_mode='categorical',
#     batch_size=32,
#     shuffle=True,
#     seed=0,
#     rotation_range=30,
#     zoom_range=0.15,
#     width_shift_range=0.2,
#     height_shift_range=0.2,
#     shear_range=0.15,
#     horizontal_flip=True,
#     fill_mode="nearest"
# )

# val_images = val_generator.flow_from_dataframe(
#     dataframe=val_df,
#     x_col='Filepath',
#     y_col='Label',
#     target_size=(224, 224),
#     color_mode='rgb',
#     class_mode='categorical',
#     batch_size=32,
#     shuffle=True,
#     seed=0
# )

# # Define the model
# pretrained_model = tf.keras.applications.MobileNetV2(
#     input_shape=(224, 224, 3),
#     include_top=False,
#     weights='imagenet',
#     pooling='avg'
# )
# pretrained_model.trainable = False

# inputs = pretrained_model.input
# x = tf.keras.layers.Dense(128, activation='relu')(pretrained_model.output)
# x = tf.keras.layers.Dense(128, activation='relu')(x)
# outputs = tf.keras.layers.Dense(len(train_df.Label.unique()), activation='softmax')(x)

# model = tf.keras.Model(inputs=inputs, outputs=outputs)

# model.compile(
#     optimizer='adam',
#     loss='categorical_crossentropy',
#     metrics=['accuracy']
# )

# # Train the model
# history = model.fit(
#     train_images,
#     validation_data=val_images,
#     epochs=5,
#     callbacks=[
#         tf.keras.callbacks.EarlyStopping(
#             monitor='val_loss',
#             patience=2,
#             restore_best_weights=True
#         )
#     ]
# )

# # Load test images
# # test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
# # test_images = test_datagen.flow_from_dataframe(
# #     dataframe=test_df,
# #     x_col='Filepath',
# #     y_col='Label',
# #     target_size=(224, 224),
# #     class_mode='categorical',
# #     shuffle=False
# # )
# # Load test images with the same preprocessing as training images
# test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
#     preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
# )

# test_images = test_datagen.flow_from_dataframe(
#     dataframe=test_df,
#     x_col='Filepath',
#     y_col='Label',
#     target_size=(224, 224),
#     class_mode='categorical',
#     shuffle=False
# )



# # Predict the labels of the test_images
# pred = model.predict(test_images)
# pred = np.argmax(pred, axis=1)

# # Map the labels
# labels = (train_images.class_indices)
# labels = dict((v, k) for k, v in labels.items())
# pred1 = [labels[k] for k in pred]

# def output(location):
#     img = load_img(location, target_size=(224, 224))
#     img = img_to_array(img)
#     img = img / 255.0
#     img = np.expand_dims(img, axis=0)
#     answer = model.predict(img)
#     y_class = answer.argmax(axis=-1)
#     res = labels[y_class[0]]  # Get the label
#     return res

# # Test the output function
# img_result = output(r"C:\Users\mas_r\OneDrive\Desktop\Major project\Dataset\test\cabbage\Image_1.jpg")
# print(img_result)

# # Save the model
# model.save('FV.h5')
import numpy as np
import pandas as pd
import os
from pathlib import Path
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

print(tf.__version__)

# Define directories using raw strings to avoid escape character issues
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

# Load Pretrained Models
vgg16_model = tf.keras.applications.VGG16(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet',
    pooling='avg'
)
vgg16_model.trainable = False

mobilenet_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet',
    pooling='avg'
)
mobilenet_model.trainable = False

# Input Layer
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

# Predict
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
