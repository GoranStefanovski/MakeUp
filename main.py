# -*- coding: utf-8 -*-

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
from base64 import b64decode
import os
import glob
from imageio import imread, imsave
import cv2
import argparse
import io
from io import BytesIO
import PIL.Image
from PIL import Image
import pymysql
import mysql.connector
# from api import mysql

n = 0
images = 'imgs/no_makeup/'

# db=pymysql.connect(host="localhost",user="root",passwd="Password12#",db="MakeUp")
# cursor=db.cursor()
# sql1='select image from images'
mydb = mysql.connector.connect(user='root',password="Password12#", host='127.0.0.1', database='MakeUp')

# Create a cursor object
cursor = mydb.cursor()

# Prepare the query
query = 'select images from images WHERE image_id = 1'

# Execute the query to get the file
cursor.execute(query)

data = cursor.fetchall()
print(data)
# The returned data will be a list of list
image = data[0][0]

# Decode the string
binary_data = b64decode(image)

# Convert the bytes into a PIL image
image = Image.open(io.BytesIO(binary_data))

# Display the image
image.show()

# # conn=mysql.connector.connect()
# cursor=conn.cursor()
# cursor.execute("select images from images WHERE image_id = 1")
# data=cursor.fetchall()
#
# image = data[0][0]
# binary_data = base64.b64decode(image)
# image = Image.open(io.BytesIO(binary_data))
# image.show()

# for image in os.listdir(images):
# for image in data:
# #     imageK = Image.open(image)
# #     data = asarray(imageK)
# #     parser = argparse.ArgumentParser()
# #     parser.add_argument('--no_makeup', type=str, default=os.path.join(images ,image ), help='path to the no_makeup image')
# #     args = parser.parse_args()
#
#
#     n += 0
#     def preprocess(img):
#         return (img / 255. - 0.5) * 2
#
#     def deprocess(img):
#         return (img + 1) / 2
#
#     batch_size = 1
#     img_size = 256
#     no_makeup = cv2.resize(data, (img_size, img_size))
#     X_img = np.expand_dims(preprocess(no_makeup), 0)
#     makeups = glob.glob(os.path.join('imgs', 'makeup', '*.*'))
#     result = np.ones((2 * img_size, (len(makeups) + 1) * img_size, 3))
#     result[img_size: 2 *  img_size, :img_size] = no_makeup / 255.
#
#     tf.reset_default_graph()
#     sess = tf.Session()
#     sess.run(tf.global_variables_initializer())
#
#     saver = tf.train.import_meta_graph(os.path.join('model', 'model.meta'))
#     saver.restore(sess, tf.train.latest_checkpoint('model'))
#
#     graph = tf.get_default_graph()
#     X = graph.get_tensor_by_name('X:0')
#     Y = graph.get_tensor_by_name('Y:0')
#     Xs = graph.get_tensor_by_name('generator/xs:0')
#
#     for i in range(len(makeups)):
#         makeup = cv2.resize(imread(makeups[i]), (img_size, img_size))
#         Y_img = np.expand_dims(preprocess(makeup), 0)
#         Xs_ = sess.run(Xs, feed_dict={X: X_img, Y: Y_img})
#         Xs_ = deprocess(Xs_)
#         result[:img_size, (i + 1) * img_size: (i + 2) * img_size] = makeup / 255.
#         result[img_size: 2 * img_size, (i + 1) * img_size: (i + 2) * img_size] = Xs_[0]
#
#         imsave(str(n)+'result.jpg', result)