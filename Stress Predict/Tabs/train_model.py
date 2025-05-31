import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Define paths
train_dir = 'dataset/train'
validation_dir = 'dataset/validation'

# Image data generator for augmentation and normalization
train_datagen = ImageDataGenerator(rescale=1.0/255.0,
                                  shear_range=0.2,
                                  zoom_range=0.2,
                                  horizontal_flip=True)

validation_datagen = ImageDataGenerator(rescale=1.0/255.0)

# Load and preprocess train and validation datasets
train_generator = train_datagen.flow_from_directory(train_dir,
                                                   target_size=(64, 64),
                                                   batch_size=32,
                                                   class_mode='binary')

validation_generator = validation_datagen.flow_from_directory(validation_dir,
                                                             target_size=(64, 64),
                                                             batch_size=32,
                                                             class_mode='binary')

# Define the CNN model
model = Sequential([
   Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
   MaxPooling2D((2, 2)),
   Conv2D(64, (3, 3), activation='relu'),
   MaxPooling2D((2, 2)),
   Conv2D(128, (3, 3), activation='relu'),
   MaxPooling2D((2, 2)),
   Flatten(),
   Dense(128, activation='relu'),
   Dropout(0.5),
   Dense(1, activation='sigmoid')  # Binary classification (stress vs. no stress)
])

model.compile(optimizer='adam',
             loss='binary_crossentropy',
             metrics=['accuracy'])

# Train the model
history = model.fit(train_generator,
                   epochs=10,
                   validation_data=validation_generator)

# Save the trained model
model.save('stress_detection_model.h5')
