### Hunter Mitchell - 06/18/2020

### Description: Full flask server side code that loads 2 pretrained deep learning models and returns predictions
###              based on the input image that the client gives



import pandas as pd
import numpy as np
import sys

from flask import Flask, request, url_for, redirect, render_template, jsonify
from tensorflow.keras.models import load_model

from PIL import Image
import base64
import re
import io
import cv2



app = Flask(__name__)



### SETTINGS ###

test_a_pic = False

show_classifying_image = False

IMG_SIZE = 256




### LOAD MODELS ###

# Current Gender Model: DenseNet201, 3000 imgs, seed 2016, epochs 10, batch size 32, img size 256, 85/15 split
gender_filename = 'kaggle_model_gender'
gender_model = load_model('/Users/huntermitchell/Documents/PYTHON_FILES/webApp/' + gender_filename)


# DO MORE EPOCHS and maybe change some other stuff
# Current Age Model: DenseNet201, 3000 imgs, seed 2016, epochs 10, batch size 32, img size 256, 85/15 split
age_filename = 'kaggle_model_age'
age_model = load_model('/Users/huntermitchell/Documents/PYTHON_FILES/webApp/' + age_filename)



if (test_a_pic == True):

    PRED_PIC_PATH = '/Users/huntermitchell/Downloads/hotgirl.jpeg'
    temp_pred_img = cv2.imread(PRED_PIC_PATH)
    temp_pred_img = temp_pred_img
    pred_img = cv2.resize(temp_pred_img,(IMG_SIZE,IMG_SIZE))
    pred_img = pred_img.reshape(1,IMG_SIZE,IMG_SIZE,3)

    age_prediction = age_model.predict(pred_img)
    print('age prediction: ', age_prediction[0,0])

    gender_prediction = gender_model.predict(pred_img)
    print('gender prediction: ', gender_prediction[0,0])





@app.route('/')
def home_get():
    return render_template('webDevProject.html')



@app.route('/', methods=['POST'])
def home_post():

    image_b64 = request.values['imageBase64']
    image_b64 = image_b64[22:] # get ride of first 22 characters
    image_bytes = base64.b64decode(image_b64) # is in bytes now 

    
    image_PIL = Image.open(io.BytesIO(image_bytes))
    #image_PIL.show() # WORKS 

    dimensions = (IMG_SIZE,IMG_SIZE)
    pred_img = image_PIL.resize(dimensions)

    pred_img = np.array(pred_img)
    pred_img = pred_img[:,:,:3]

    if show_classifying_image == True:
        test_img = Image.fromarray(pred_img) # Does not support [0,1] images in RGB
        test_img.show() # This is the exact image that the model is classifying ! 


    pred_img = pred_img.reshape(1,IMG_SIZE,IMG_SIZE,3)
    
    #print(pred_img[0])
    #print(pred_img.shape)

    if 'gender' == request.values['predType']:
        prediction = gender_model.predict(pred_img)

        male_prob =  round(prediction[0,0] * 100 , 2)
        female_prob = round( ( 1 - prediction[0,0]) * 100 , 2)
        
        combinedString = 'Male Probability: ' + str(male_prob) + '%, Female Probability: ' + str(female_prob) + '%'


    if 'age' == request.values['predType']:
        prediction = age_model.predict(pred_img)
        combinedString =  str( (int) (prediction[0,0]) ) + ' years old!'


    #print(combinedString)
    
    return combinedString

        

if __name__ == "__main__":
    app.run()



# to run: python3 webDevProjectBackEnd.py