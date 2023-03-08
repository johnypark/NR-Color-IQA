#!python

import pandas as pd
import tensorflow as tf
import os
import sys
import time
import glob
import NR_Color_IQA as iqa
import numpy as np

def main(glob_PATH, out_fileName, RESIZE_RESOL = 512):
    
    QICI_colorful = []
    BRISQUE = []
    UCIQE = []
    img_fileName = []
    collectionCode =[]

    print(glob_PATH)
    ls_all_files = glob.glob(glob_PATH+"*/*.jpg")
    print(ls_all_files)
    print(out_fileName)
    for file_name in ls_all_files:

        start = time.time()
        print('Reading file from PATH:{}'.format(file_name))        
        tens = tf.keras.utils.load_img(file_name)
        tens = np.array(tens)
        #print(tens)
        tens = tf.image.resize(tens, (RESIZE_RESOL, RESIZE_RESOL))
        img_fileName += [file_name.split("/")[-1]]
        collectionCode +=[file_name.split("/")[-2]]
        QICI_colorful += [iqa.get_colorfulness()(tens).numpy()]
        BRISQUE += [iqa.brisque(tens.numpy()).tolist()] 
        UCIQE += [iqa.get_uciqe(tens.numpy())]
        end = time.time()
        print("Time to run: {}".format((end - start)))
    
    df_part1 = pd.DataFrame({'file_name':img_fileName, 'QICI_colorful': QICI_colorful, 
              'UCIQE':UCIQE, 'collectionCode': collectionCode})
    df_part2 = pd.DataFrame(BRISQUE, columns = iqa.get_brisque_colnames(['brisque']))
    df_out = pd.concat([df_part1, df_part2], axis = 1)
    
    try:
        df_out.to_csv(out_fileName+'.csv')
    except:
        satisfy = True
        out_fileName = out_fileName+"_1"                
        while satisfy:
                try:
                    df_out.to_csv(out_fileName)
                    satisfy = False
                except:
                    out_fileName = out_fileName+"_1"                                    

if __name__ == '__main__':
    
    glob_PATH = sys.argv[1]
    try:
        out_fileName = sys.argv[2]
    except:
        out_fileName = 'get_metrics_out'
    print(out_fileName)
    main(glob_PATH, out_fileName)