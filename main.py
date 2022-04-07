# -*- coding: utf-8 -*-

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
from base64 import b64decode
import os
import glob
from imageio import imread, imsave
import cv2
import io
from io import BytesIO
import PIL.Image
from PIL import Image
import pymysql
import mysql.connector

n = 1
# Fill the credentials of the database
config = {
    'user': 'root',
    'password': '123456',
    'host': '127.0.0.1',
    'database': 'makeup',
}

mydb = mysql.connector.connect(**config)

# Create a cursor object
cursor = mydb.cursor()

#Inert the database fields
table_name = 'pictures'
id_collumn_name = 'image_id'
collumn_name = 'image'

query1 = 'SELECT * FROM ' + table_name

cursor.execute(query1)

numberOfPictures = cursor.fetchall()


for n in range(1,len(numberOfPictures)+1):

    # Prepare the query
    

    query = "SELECT " + collumn_name + " FROM " + table_name + " WHERE " + id_collumn_name + " = " + str(n)

    # Execute the query to get the file
    cursor.execute(query)

    data = cursor.fetchall()

    # The returned data will be a list of list
    image = data[0][0]

    # Decode the string
    binary_data = b64decode(image)

    # Convert the bytes into a PIL image
    image = Image.open(io.BytesIO(binary_data))

    # image.show()
    # Convert the PIL image into a numpy array
    image = np.array(image)

    #Processing the picture
    def preprocess(img):
        return (img / 255. - 0.5) * 2

    def deprocess(img):
        return (img + 1) / 2

    batch_size = 1
    img_size = 256
    no_makeup = cv2.resize(image, (img_size, img_size))
    X_img = np.expand_dims(preprocess(no_makeup), 0)
    makeups = glob.glob(os.path.join('imgs', 'makeup', '*.*'))
    result = np.ones((2 * img_size, (len(makeups) + 1) * img_size, 3))
    result[img_size: 2 *  img_size, :img_size] = no_makeup / 255.

    tf.reset_default_graph()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    saver = tf.train.import_meta_graph(os.path.join('model', 'model.meta'))
    saver.restore(sess, tf.train.latest_checkpoint('model'))

    graph = tf.get_default_graph()
    X = graph.get_tensor_by_name('X:0')
    Y = graph.get_tensor_by_name('Y:0')
    Xs = graph.get_tensor_by_name('generator/xs:0')

    for i in range(len(makeups)):
        makeup = cv2.resize(imread(makeups[i]), (img_size, img_size))
        Y_img = np.expand_dims(preprocess(makeup), 0)
        Xs_ = sess.run(Xs, feed_dict={X: X_img, Y: Y_img})
        Xs_ = deprocess(Xs_)
        result[:img_size, (i + 1) * img_size: (i + 2) * img_size] = makeup / 255.
        result[img_size: 2 * img_size, (i + 1) * img_size: (i + 2) * img_size] = Xs_[0]

        imsave(str(n)+'_result.jpg', result)
    n += 1
