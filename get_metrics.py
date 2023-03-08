#!python

import pandas as pd
import tensorflow as tf
import os
import sys
import time
import glob
import NR_Color_IQA as iqa
import numpy as np


QICI_colorful = []
BRISQUE = []
UCIQE = []
img_filename = []
glob_PATH = sys.argv[1]
RESIZE_RESOL = 512

def main():
    
    QICI_colorful = []
    BRISQUE = []
    UCIQE = []
    img_fileName = []
    print(glob_PATH)
    ls_all_files = glob.glob(glob_PATH+"*/*.jpg")
    print(ls_all_files)
    for file_name in ls_all_files:

        start = time.time()
        print('Reading file from PATH:{}'.format(file_name))        
        tens = tf.keras.utils.load_img(file_name)
        tens = np.array(tens)
        #print(tens)
        tens = tf.image.resize(tens, (RESIZE_RESOL, RESIZE_RESOL))
        img_fileName += [file_name.split("/")[-1]]
        QICI_colorful += [iqa.get_colorfulness()(tens).numpy()]
        BRISQUE += [iqa.brisque(tens.numpy()).tolist()] 
        UCIQE += [iqa.get_uciqe(tens.numpy())]
        end = time.time()
        print("Time to run: {}".format((end - start)))
    
    df_part1 = pd.DataFrame({'file_name':img_fileName, 'QICI_colorful': QICI_colorful, 
              'UCIQE':UCIQE})
    df_part2 = pd.DataFrame(BRISQUE, columns = iqa.get_brisque_colnames(['brisque']))
    pd.concat([df_part1, df_part2], axis = 1).to_csv('get_metrics_out.csv')

if __name__ == '__main__':
    main()