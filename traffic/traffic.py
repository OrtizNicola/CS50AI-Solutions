import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []
    # We iterate through the folders in the data directory
    print("Started loading the data!!!")
    for dir in os.listdir(data_dir):
        # Check if we are in a directory, not any other type of file like a .Ds_store
        if os.path.isdir(os.path.join(data_dir, dir)):
            # For each folder, we iterate through all of the images there
            for image in os.listdir(os.path.join(data_dir, dir)):
                # Read the image
                img = cv2.imread(os.path.join(data_dir, dir, image))
                # Add the resized image to the list of data
                images.append(cv2.resize(img, dsize = (IMG_WIDTH, IMG_HEIGHT)))
                # Add the label for that image 
                labels.append(int(dir))
    print("All folders loaded!!!")
    return (images, labels)

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Define the neural network
    model = tf.keras.models.Sequential()
    # This layer rescales the values of each pixel bringing the values to a range of [0, 1]
    model.add(tf.keras.layers.experimental.preprocessing.Rescaling(scale=1.0 / 255, input_shape=(30, 30, 3)))
    # The convolutional layer applies 32 different filteres to the image so it can detect different features
    model.add(tf.keras.layers.Conv2D(16, (6, 6), activation='relu'))
    # Pooling makes the data simpler so that we don't care about each pixel, just about more some areas of the image
    model.add(tf.keras.layers.MaxPooling2D((2, 2)))
    # After applying all of the convolution step, we bring the data to the neural network
    model.add(tf.keras.layers.Flatten())
    # The dropout technique helps to avoid overfittinig, so the model can perform better in the testing set
    model.add(tf.keras.layers.Dropout(0.5))
    # we add a hidden layer to the neural network
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    # we add another hidden layer to the neural network
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    # The final layer will tell us the predicted result for our input, we have 43 different possibilities
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')) 
    # Assign the criteria that the model will use to train on the training set
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

if __name__ == "__main__":
    main()
