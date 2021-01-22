''' 
# -*- coding: UTF-8 -*-
'''
from __future__ import print_function
import config.config as cfg

import sys
import os
import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(BASE_DIR)
sys.path.append(ROOT_DIR)


class livox_model():
    def __init__(self, height, width,channels):
        self.img_height = height
        self.img_width = width
        self.channels = channels

    def placeholder_inputs(self, batch_size):

        input_bev_img_pl = tf.placeholder(tf.bool,
                                          shape=(batch_size, self.img_height, self.img_width, self.channels))

        return input_bev_img_pl

    def res_yolo(self, inputs, filters, res_num):
        inputs = slim.conv2d(inputs, filters, [3, 3])
        inputs = slim.max_pool2d(inputs, [2, 2])
        for i in range(res_num):
            shortcut = inputs
            inputs = slim.conv2d(inputs, filters/2, [1, 1])
            inputs = slim.conv2d(inputs, filters, [3, 3])
            inputs = inputs + shortcut
        return inputs

    def livox_detection(self,input_bev_img_pl,end_points):

        with slim.arg_scope([slim.conv2d,slim.fully_connected],
                     normalizer_fn=slim.batch_norm,
                     normalizer_params={'is_training':False,'decay':0.95},
                     trainable = False
                   ):
            with slim.arg_scope([slim.conv2d],padding='SAME',
                    ):
                bev_input = tf.cast(input_bev_img_pl,dtype=tf.float32)
                print (bev_input.shape) 
                img_conv1 = slim.conv2d(bev_input,64,[3,3])
                img_conv2 = self.res_yolo(img_conv1,64,1)

                img_conv3 = self.res_yolo(img_conv2,128,2)

                img_conv4 = self.res_yolo(img_conv3,256,4)

                img_conv5 = self.res_yolo(img_conv4,512,4)

                img_conv6 = self.res_yolo(img_conv5,1024,2)

                img_conv6 = slim.conv2d(img_conv6,512,[1,1])
                img_conv6 = slim.conv2d(img_conv6,1024,[3,3])
                img_conv6 = slim.conv2d(img_conv6,512,[1,1])

                img_conv6 = slim.conv2d(img_conv6,256,[1,1])

                img_deconv_6 = tf.image.resize_bilinear(img_conv6,\
                    [int(self.img_height/16),int(self.img_width/16)])
                
                img_deconv_5 = tf.concat([img_conv5 , img_deconv_6],3) 
                img_deconv_5 = slim.conv2d(img_deconv_5,256,[1,1])
                img_deconv_5 = slim.conv2d(img_deconv_5,512,[3,3])
                img_deconv_5 = slim.conv2d(img_deconv_5,256,[1,1])
                img_deconv_5 = slim.conv2d(img_deconv_5,128,[1,1])
                

                img_deconv_5 = tf.image.resize_bilinear(img_deconv_5,\
                    [int(self.img_height/8),int(self.img_width/8)])
                img_deconv_4 = tf.concat([img_conv4 , img_deconv_5],3) 
                img_deconv_4 = slim.conv2d(img_deconv_4,128,[1,1])
                img_deconv_4 = slim.conv2d(img_deconv_4,256,[3,3])
                img_deconv_4 = slim.conv2d(img_deconv_4,128,[1,1])

                feature_out = slim.conv2d(img_deconv_4,128,[3,3])

                feature_out = slim.conv2d(feature_out,19,[3,3],\
                    normalizer_fn=None,activation_fn=None)
                end_points['feature_out'] = feature_out

        return end_points

    def get_model(self, input_bev_img_pl):
        end_points = {}
        end_points = self.livox_detection(input_bev_img_pl, end_points)

        return end_points
