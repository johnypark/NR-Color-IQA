#!python

'''
Getting underwater color image quality evaluation metric, UCIQE 
Modified from original code of Xuelei Chen (chenxuelei@hotmail.com)
https://github.com/xueleichen/PSNR-SSIM-UCIQE-UIQM-Python/blob/main/nevaluate.py

'''
import numpy as np
import math
import sys
from skimage import io, color, filters
import os
import math
import pandas as pd
import time

def get_uciqe(a):
    print('Calcuating UCIQE....\n')
    rgb = a
    lab = color.rgb2lab(a)
    gray = color.rgb2gray(a)
    # UCIQE
    c1 = 0.4680
    c2 = 0.2745
    c3 = 0.2576
    l = lab[:,:,0]

    #1st term
    chroma = (lab[:,:,1]**2 + lab[:,:,2]**2)**0.5
    uc = np.mean(chroma)
    sc = (np.mean((chroma - uc)**2))**0.5

    #2nd term
    top = np.array(np.round(0.01*l.shape[0]*l.shape[1]), dtype =int)
    sl = np.sort(l,axis=None)
    isl = sl[::-1]
    conl = np.mean(isl[:top])-np.mean(sl[:top])

    #3rd term
    satur = []
    chroma1 = chroma.flatten()
    l1 = l.flatten()
    for i in range(len(l1)):
        if chroma1[i] == 0: satur.append(0)
        elif l1[i] == 0: satur.append(0)
        else: satur.append(chroma1[i] / l1[i])

    us = np.mean(satur)

    uciqe = c1 * sc + c2 * conl + c3 * us
    print('Done.\n')
    
    return uciqe

def main():
    result_path = sys.argv[1]
    all_argu = sys.argv[1:]
    for result_path in all_argu:

        result_dirs = os.listdir(result_path)

        sumuiqm, sumuciqe = 0.,0.
        fileName =[]
        UIQM = []
        UCIQE = []
        N=0
        for file_name in result_dirs:
            if '.jpg' in file_name:
                #corrected image
                                
                start = time.time()
                fPATH = os.path.join(result_path, file_name)
                print('Reading file from PATH:{}'.format(fPATH))
                corrected = io.imread(fPATH)

                uciqe = get_uciqe(corrected)

                UCIQE += [uciqe]
                fileName += [file_name]
                end = time.time()
                print("Time to run: {}".format((end - start)))
                
        pd.DataFrame.from_dict({'file_name':fileName, #'uiqm':UIQM, 
                                'uciqe':UCIQE, 'collectionCode':result_path}).to_csv("herb2022_test_ui_metrics_"+result_path+".tsv", sep="\t")
if __name__ == '__main__':
    main()