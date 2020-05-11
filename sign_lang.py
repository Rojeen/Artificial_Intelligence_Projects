import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
'''
from sklearn.metrics         import accuracy_score
from sklearn.model_selection import train_test_split

import keras
from keras.utils  import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
'''
'''
class SignLanguage:
    def __init__(self):
        self.model = None
        
        self.data = {
            "train": None,
            "test" : None
        }
        self.create_model()
    
    def create_model(self):
        """
        Create a CNN model and save it to self.model
        """
        # You will generate a keras sequential mode here
        # Make sure to set the self.model variable with your compiled sequential model.
        
        # TODO: Create a Sequential model
        model = Sequential() 
            
        # TODO: Compile the model with categorical_crossentropy
        model.compile('adam', loss=keras.losses.categorical_crossentropy, metrics=['accuracy'])
        
        self.model = model
    
    def prepare_data(self, images, labels):
        """
        Use this method to normalize the dataset and split it into train/test.
        Save your data in self.data["train"] and self.data["test"] as a tuple
        of (images, labels)
        
        :param images numpy array of size (num_examples, 28*28)
        :param labels numpy array of size (num_examples, )
        """
        # TODO : split into training and validation set
        # TODO : reshape each example into a 2D image (28, 28, 1)
        
        """
        Mainly this splits the data into training and validation sets. 
        You may choose to normalize or downsample your data here, as well.
        """

        x_train, x_test, y_train, y_test = train_test_split(images, labels) # see if I need to add any more parameters

        self.data = {
            "train": (x_train, y_train), # (x_train, y_train)
            "test" : (x_test, y_test), # (x_test, y_test)
        }
    
    def train(self, batch_size:int=128, epochs:int=50, verbose:int=1):
        """
        Use model.fit() to train your model. Make sure to return the history for a neat visualization.
        
        :param batch_size The batch size to use for training
        :param epochs     Number of epochs to use for training
        :param verbose    Whether or not to print training output
        """

        """
        This method invokes the training of the model. Make sure to return the 
        generated history object. Your model will be trained for a max of 50 
        epochs during grading. Make sure you are using the input parameters 
        (batch size, epochs, verbose)
        """

        history = model.fit(data, labels, epochs, batch_size) # TODO: figure out where to get labels

        if verbose:
          print(history)

        return history
    
    def predict(self, data):
        """
        Use the trained model to predict labels for test data.
        
        :param data: numpy array of test images
        :return a numpy array of test labels. array size = (num_examples, )
        """
        
        # Don't forget to normalize the data in the same way as training data
        # self.model.predict() and np.argmax( , axis=1) might help
        
        

        return np.zeros(data.shape[0])
    
    def visualize_data(self, data):
        """
        Visualizing the hand gestures
        
        :param data: numpy array of images
        """
        if data is None: return
        
        nrows, ncols = 5, 5
        fig, axs = plt.subplots(nrows, ncols, figsize=(10, 10), sharex=True, sharey=True)
        plt.subplots_adjust(wspace=0, hspace=0)

        for i in range(nrows):
            for j in range(ncols):
                axs[i][j].imshow(data[0][i*ncols+j].reshape(28, 28), cmap='gray')
        plt.show()

    def visualize_accuracy(self, history):
        """
        Plots out the accuracy measures given a keras history object
        
        :param history: return value from model.fit()
        """
        if history is None: return
        
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title("Accuracy")
        plt.xlabel('epoch')
        plt.ylabel('accuracy')
        plt.legend(['train','test'])
        plt.show()
'''

if __name__=="__main__":

	# get dataframes for train and test
    train = pd.read_csv('train.csv')
    test  = pd.read_csv('test.csv')

    #print(train.head())
    # create 1D arrays with just labels (train_labels and test_labels)
    train_labels, test_labels = train['label'].values, test['label'].values
    print(train_labels)
    # drop the labels column from train and test dataframes
    train.drop('label', axis=1, inplace=True)
    test.drop('label', axis=1, inplace=True)

    #print(train.head())
    # determine number of classes
    num_classes = test_labels.max() + 1
    print(num_classes)
    # create image arrays for train and test set
    train_images, test_images = train.values, test.values

    for i in range(train_images.shape[0]):
          np.reshape(train_images[i], (28, 28, 1))
    #28*28=784
    # outputs: (11059, 784) (11059,) (7172, 784) (7172,)
    #print(train_images[0])
    #print(train_images[0].shape)
    print(train_images.shape, train_labels.shape, test_images.shape, test_labels.shape)