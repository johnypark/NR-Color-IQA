"""
forked from https://github.com/buyizhiyou/NRVQA/blob/master/brisque.py
Author: @buyizhiyou

"""

import math
import scipy.special
import numpy as np
import cv2
import scipy as sp



brisque_features = ['GGD_shape','GGD_var', # f1 -f2
'AGGD_H_shape', 'AGGD_H_mean', 'AGGD_H_lvar', 'AGGD_H_rvar', #f3-f6
'AGGD_V_shape', 'AGGD_V_mean', 'AGGD_V_lvar', 'AGGD_V_rvar', #f7-f10
'AGGD_D1_shape', 'AGGD_D1_mean', 'AGGD_D1_lvar', 'AGGD_D1_rvar', #f11-f14
'AGGD_D2_shape', 'AGGD_D2_mean', 'AGGD_D2_lvar', 'AGGD_D2_rvar'] #f15-f18

def get_brisque_colnames(list_names, colname_type = 'full'):

    def brisque_listcomp(list_names, feature_names):
        colname =[]
        for name in list_names:
            colname += [name+"_"+ ft_name for ft_name in feature_names]
        return colname
    
    if len(list_names) == 1:
        brisque_f_nums = ["f"+ str(k) for k in range(1, 37)]
        outcome = [list_names[0]+"_"+ft_name for ft_name in brisque_f_nums]

    else:    
        if colname_type == 'full':
            outcome = brisque_listcomp(list_names, feature_names = brisque_features)  

        elif colname_type == 'short':
            brisque_f_nums = ["f"+ str(k) for k in range(1, 19)]
            outcome = brisque_listcomp(list_names, feature_names = brisque_f_nums)

    
    return outcome



gamma_range = np.arange(0.2, 10, 0.001)
a = scipy.special.gamma(2.0/gamma_range)
a *= a
b = scipy.special.gamma(1.0/gamma_range)
c = scipy.special.gamma(3.0/gamma_range)
prec_gammas = a/(b*c)


def aggd_features(imdata):
    # flatten imdata
    imdata.shape = (len(imdata.flat),)
    imdata2 = imdata*imdata
    left_data = imdata2[imdata < 0]
    right_data = imdata2[imdata >= 0]
    left_mean_sqrt = 0
    right_mean_sqrt = 0
    if len(left_data) > 0:
        left_mean_sqrt = np.sqrt(np.average(left_data))
    if len(right_data) > 0:
        right_mean_sqrt = np.sqrt(np.average(right_data))

    if right_mean_sqrt != 0:
        gamma_hat = left_mean_sqrt/right_mean_sqrt
    else:
        gamma_hat = np.inf
    # solve r-hat norm

    imdata2_mean = np.mean(imdata2)
    if imdata2_mean != 0:
        r_hat = (np.average(np.abs(imdata))**2) / (np.average(imdata2))
    else:
        r_hat = np.inf
    rhat_norm = r_hat * (((math.pow(gamma_hat, 3) + 1) *
                          (gamma_hat + 1)) / math.pow(math.pow(gamma_hat, 2) + 1, 2))

    # solve alpha by guessing values that minimize ro
    pos = np.argmin((prec_gammas - rhat_norm)**2)
    alpha = gamma_range[pos]

    gam1 = scipy.special.gamma(1.0/alpha)
    gam2 = scipy.special.gamma(2.0/alpha)
    gam3 = scipy.special.gamma(3.0/alpha)

    aggdratio = np.sqrt(gam1) / np.sqrt(gam3)
    bl = aggdratio * left_mean_sqrt
    br = aggdratio * right_mean_sqrt

    # mean parameter
    N = (br - bl)*(gam2 / gam1)  # *aggdratio
    return (alpha, N, bl, br, left_mean_sqrt, right_mean_sqrt)


def paired_product(new_im):
    shift1 = np.roll(new_im.copy(), 1, axis=1)
    shift2 = np.roll(new_im.copy(), 1, axis=0)
    shift3 = np.roll(np.roll(new_im.copy(), 1, axis=0), 1, axis=1)
    shift4 = np.roll(np.roll(new_im.copy(), 1, axis=0), -1, axis=1)

    H_img = shift1 * new_im
    V_img = shift2 * new_im
    D1_img = shift3 * new_im
    D2_img = shift4 * new_im

    return (H_img, V_img, D1_img, D2_img)


def calculate_mscn(dis_image):
    dis_image = dis_image.astype(np.float32) 
    ux = cv2.GaussianBlur(dis_image, (7, 7), 7/6)
    ux_sq = ux*ux
    sigma = np.sqrt(np.abs(cv2.GaussianBlur(dis_image**2, (7, 7), 7/6)-ux_sq))

    mscn = (dis_image-ux)/(1+sigma)

    return mscn


def ggd_features(imdata):
    nr_gam = 1/prec_gammas
    sigma_sq = np.var(imdata)
    E = np.mean(np.abs(imdata))
    rho = sigma_sq/E**2
    pos = np.argmin(np.abs(nr_gam - rho))
    return gamma_range[pos], sigma_sq


def extract_brisque_feats(mscncoefs):
    alpha_m, sigma_sq = ggd_features(mscncoefs.copy())
    pps1, pps2, pps3, pps4 = paired_product(mscncoefs)
    alpha1, N1, bl1, br1, lsq1, rsq1 = aggd_features(pps1)
    alpha2, N2, bl2, br2, lsq2, rsq2 = aggd_features(pps2)
    alpha3, N3, bl3, br3, lsq3, rsq3 = aggd_features(pps3)
    alpha4, N4, bl4, br4, lsq4, rsq4 = aggd_features(pps4)
    # print(alpha_m, alpha1)
    return [
        alpha_m, sigma_sq,
        alpha1, N1, lsq1**2, rsq1**2,  # (V)
        alpha2, N2, lsq2**2, rsq2**2,  # (H)
        alpha3, N3, lsq3**2, rsq3**2,  # (D1)
        alpha4, N4, lsq4**2, rsq4**2,  # (D2)
    ]


def brisque(im):
    mscncoefs = calculate_mscn(im)
    features1 = extract_brisque_feats(mscncoefs)
    lowResolution = cv2.resize(im, (0, 0), fx=0.5, fy=0.5)
    features2 = extract_brisque_feats(lowResolution)

    return np.array(features1+features2)