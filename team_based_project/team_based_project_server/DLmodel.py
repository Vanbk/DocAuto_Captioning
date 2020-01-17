from keras.layers import LSTM, Embedding, TimeDistributed, Dense, RepeatVector,\
                         Activation, Flatten, Reshape, concatenate, Dropout, BatchNormalization
from keras.optimizers import Adam, RMSprop
from keras.models import Model
from keras import Input, layers
from keras.layers.merge import add
from keras.preprocessing.sequence import pad_sequences
import string
import glob
import  os
import numpy
import numpy as np
import matplotlib.pyplot as plt

from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing import image

max_length = 34
vocab_size = 1652
embedding_dim = 200

# Construct model
inputs1 = Input(shape=(2048,)) # embedded image input
fe1 = Dropout(0.5)(inputs1)
fe2 = Dense(256, activation='relu')(fe1)
inputs2 = Input(shape=(max_length,)) # word embedding input 
se1 = Embedding(vocab_size, embedding_dim, mask_zero=True)(inputs2)
se2 = Dropout(0.5)(se1)
se3 = LSTM(256)(se2)
decoder1 = add([fe2, se3])
decoder2 = Dense(256, activation='relu')(decoder1)
outputs = Dense(vocab_size, activation='softmax')(decoder2)
model = Model(inputs=[inputs1, inputs2], outputs=outputs)
model.load_weights("./deep_learning_application/model_30.h5")

# load dictionary
filename = "./deep_learning_application/vocab.txt"
#open the file as read only
file = open(filename, 'r')
#read all text
doc = file.read()
#close the file
file.close()
vocab = doc.split('\n')

# create index toword and word to index table
ixtoword = {}
wordtoix = {}
ix = 1

for w in vocab:
    wordtoix[w] = ix
    ixtoword[ix] = w  # index to word
    ix += 1
    
# Model for encoding image
# Load the Inception v3 model
model_IV3 = InceptionV3(weights='imagenet')
# eliminate the last Layer
model_new = Model(model_IV3.input, model_IV3.layers[-2].output)

# Load image with specific size required by Inception v3
def preprocess(image_path):
    # size 299x299
    img = image.load_img(image_path, target_size=(299, 299))
    # convert PIL image to numpy array for 3-dimensions
    x = image.img_to_array(img)
    # add one more dimension
    x = np.expand_dims(x, axis = 0)
    # preprocess the images using preprocessing_input()
    x = preprocess_input(x)
    return x

# Image Embedding to vector(2048, )
def encode(image):
    image = preprocess(image) # preprocess
    fea_vec = model_new.predict(image) # get the encoding vector
    # reshape from (1, 2048) to (2048, )
    fea_vec = np.reshape(fea_vec, fea_vec.shape[1])
    return fea_vec

def greedySearch(photo):
    in_text = 'startseq'
    for i in range(max_length):
        sequence = [wordtoix[w] for w in in_text.split() if w in wordtoix]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo,sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = ixtoword[yhat]
        in_text += ' ' + word
        if word == 'endseq':
            break
    final = in_text.split()
    final = final[1:-1]
    final = ' '.join(final)
    return final

def generateCaption(imgPath):
    imgPath = './deep_learning_application/extracted_image/' + imgPath
    x = encode(imgPath)
    x = x.reshape(1,2048)
    caption = greedySearch(x)
    return caption
    
def generateAll(listOfImg):
    listOfCaption = list()
    for img in listOfImg:
        listOfCaption.append(generateCaption(img))
    return listOfCaption
    


