'''This script goes along the blog post
"Building powerful image classification models using very little data"
from blog.keras.io.
It uses data that can be downloaded at:
https://www.kaggle.com/c/dogs-vs-cats/data
In our setup, we:
- created a data/ folder
- created train/ and validation/ subfolders inside data/
- created cats/ and dogs/ subfolders inside train/ and validation/
- put the cat pictures index 0-999 in data/train/cats
- put the cat pictures index 1000-1400 in data/validation/cats
- put the dogs pictures index 12500-13499 in data/train/dogs
- put the dog pictures index 13500-13900 in data/validation/dogs
So that we have 1000 training examples for each class, and 400 validation examples for each class.
In summary, this is our directory structure:
```
data/
    train/
        dogs/
            dog001.jpg
            dog002.jpg
            ...
        cats/
            cat001.jpg
            cat002.jpg
            ...
    validation/
        dogs/
            dog001.jpg
            dog002.jpg
            ...
        cats/
            cat001.jpg
            cat002.jpg
            ...
```
'''

import argparse
import json

from keras import applications
from keras import backend as K
from keras.callbacks import TensorBoard
from keras.layers import Dropout, Flatten, Dense
from keras.models import Sequential, Model
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator

# Import functions for creating data generators and training model,
# those are the same and can be reused. Great!
from small_convnet_1 import create_data_generators, train_model

def create_model(args):
    input_shape = (params.img_height, params.img_width, 3)

    # build the VGG16 network
    base_model = applications.VGG16(weights='imagenet', include_top=False, input_shape=input_shape)

    # build a classifier model to put on top of the convolutional model
    top_model = Sequential()
    top_model.add(Flatten(input_shape=base_model.output_shape[1:]))
    top_model.add(Dense(256, activation='relu'))
    top_model.add(Dropout(params.drop_rate))
    top_model.add(Dense(1, activation='sigmoid'))

    # note that it is necessary to start with a fully-trained
    # classifier, including the top classifier,
    # in order to successfully do fine-tuning
    top_model.load_weights(params.top_path)

    # add the model on top of the convolutional base
    model = Model(inputs=base_model.input, outputs=top_model(base_model.output))

    # set the first 25 layers (up to the last conv block)
    # to non-trainable (weights will not be updated)
    for layer in model.layers[1:15]:
        layer.trainable = False

    # compile the model with a SGD/momentum optimizer
    # and a very slow learning rate.
    model.compile(loss='binary_crossentropy',
                  optimizer=SGD(lr=params.learning_rate, momentum=0.9),
                  metrics=['accuracy'])

    return model

def main(params):
    model = create_model(params)

    train_generator, validation_generator = create_data_generators(params)

    history = train_model(model, train_generator, validation_generator, params)

    json.dump(history.history, open(params.metrics_path, 'w'))
    model.save_weights(params.save_path)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--train_data_dir', type=str, default='data/train',
                        help="Path to directory with training data.")
    parser.add_argument('--nb_train_samples', type=int, default=2000,
                        help="Number of training samples.")
    parser.add_argument('--val_data_dir', type=str, default='data/validation',
                        help="Path to directory with test data.")
    parser.add_argument('--nb_val_samples', type=int, default=800,
                        help="Number of test samples.")
    parser.add_argument('--img_height', type=int, default=150,
                        help="Images will be resized to this height.")
    parser.add_argument('--img_width', type=int, default=150,
                        help="Images will be resized to this width.")
    parser.add_argument('--epochs', type=int, default=50,
                        help="Epochs of training.")
    parser.add_argument('--batch_size', type=int, default=16,
                        help="Batch size.")
    parser.add_argument('--workers', type=int, default=4,
                        help="Maximum number of that will execute the generator.")
    parser.add_argument('--learning_rate', type=float, default=0.0001,
                        help="Momentum(0.9) learning rate.")
    parser.add_argument('--drop_rate', type=float, default=0.5,
                        help="Dense layer dropout rate.")
    parser.add_argument('--shear_range', type=float, default=0.2,
                        help="Shear intensity (angle) in counter-clockwise direction in degrees.")
    parser.add_argument('--zoom_range', type=float, default=0.2,
                        help="Range for random zoom: [1 - zoom_range, 1 + zoom_range].")
    parser.add_argument('--log_dir', type=str, default='logs/vgg',
                        help="Where to save TensorBoard logs.")
    parser.add_argument('--metrics_path', type=str, default='vgg_metrics.json',
                        help="Where to save json with metrics after training.")
    parser.add_argument('--top_path', type=str, default='fc_model.h5',
                        help="Where to load the top model weights from.")
    parser.add_argument('--save_path', type=str, default='vgg_model.h5',
                        help="Where to save model weights after training.")
    params = parser.parse_args()

    main(params)
