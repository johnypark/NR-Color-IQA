#!python

""" Colorfulness - CIQI and CQE
"""

import tensorflow as tf

def get_colorfulness(metric_type = 'CIQI'):

    def apply(input_image):
        #check if input dimension is 3

        rgyb_matrix = tf.reshape(tf.constant([[1, -1, 0, 0.5, 0.5, -1]]), (2,3))
        input_rgyb = tf.matmul(input_image, tf.transpose(rgyb_matrix))
        mu_rg, mu_yb = tf.reduce_mean(input_rgyb, axis = (0,1))
        std_rg, std_yb = tf.math.reduce_std(input_rgyb, axis = (0,1))
        #print(mu_rg, mu_yb, std_rg, std_yb)

        if metric_type == 'CIQI':
            colorfulness = tf.math.sqrt((std_rg**2+std_yb**2))+0.3*tf.math.sqrt((mu_rg**2+mu_yb**2))/(85.59)

        elif metric_type == 'CQE':
            colorfulness = 0.02*tf.math.log(std_rg**2/tf.math.abs(mu_rg)**0.2)*tf.math.log(std_yb**2/tf.math.abs(mu_yb)**0.2)
            
        return colorfulness

    return apply
