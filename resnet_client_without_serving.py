import PIL
from keras.preprocessing.image import load_img 
from keras.preprocessing.image import img_to_array 
import numpy as np 
import tensorflow as tf
import time

## The image PATH is the location of the image
IMAGE_PATH = '/tmp/cat.jpg'

## Local model PATH
MODEL_PATH = '/tmp/resnet/1538687457'

def main():
  ## Load an image in PIL format 
  original = load_img(IMAGE_URL, target_size = (224, 224)) 

  ## Convert the PIL image to a numpy array 
  numpy_image = img_to_array(original) 

  x = tf.keras.applications.resnet.preprocess_input(numpy_image)
  x = np.array(open(IMAGE_URL,"rb").read())

  ## Load model
  model = tf.saved_model.load(MODEL_PATH)

  ## Send few requests to warm-up the model.
  for _ in range(3):
    response = model.signatures["predict"](tf.constant([x]))
    
  ## Predict
  num_requests = 10
  start = time.time()
  for _ in range(num_requests):
    response = model.signatures["predict"](tf.constant([x]))

  total_time = time.time()-start
  print('avg latency: {} ms'.format((total_time*1000)/num_requests))

if __name__ == '__main__':
  main()
