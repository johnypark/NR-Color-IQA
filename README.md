# NR-Color-IQA
 No reference Color Image Quality Metrics

## Reference
1. [UCIQE: An Underwater Color Image Quality Evaluation Metric, 2015](10.1109/TIP.2015.2491020)
2. [BRISQUE: No-refence image quality assessment in the spatial domain, 2012](10.1109/TIP.2012.2214050)
3. NIQE
4. PIQE
5. CRME: [No reference color image contrast and quality measures (IEEE Transactions on Consumer Electronics)](10.1109/TCE.2013.6626251)
6. CIQI (Color Image Quality Index): [Color image quality measures and retrieval](https://digitalcommons.njit.edu/dissertations/745/)
7. [A new image quality measure for assessment of histogram equalization-based contrast enhancement techniques](https://www.sciencedirect.com/science/article/abs/pii/S1051200412000747)
8. [Evaluation of color differences in natural scene color images](https://www.sciencedirect.com/science/article/pii/S0923596518301863)
9. [No-reference color image quality assessment: from entropy to perceptual quality](https://jivp-eurasipjournals.springeropen.com/articles/10.1186/s13640-019-0479-7)

## DataSets

KonIQ-10K: An Ecologically Valid Database of Deep Learning of Blind Image Quality Assessment (IEEE Transactions on Image Processing)
KANDID-10K: A Large-scale Artificially Distorted IQA Database  ( QoMEX IEEE )
KANDIS-700K dataset



a = R − G (1)
β = 0.5 × (R + G) − B (2)
CIQI = c1 × CIQI_colorfulness + c2× CIQI_sharpness + c3 × CIQI_contrast (3)
CIQI_colorfulness = (sqrt(stdev(alpha)^2+stdev(beta)^2) + 0.3*sqrt(mu(alpha)^2+mu(beta)^2)) / 85.59
CIQI_sharpness = 1 − (1 − (tep_estimated − tep_sobel)/tep_sobel)**0.2
CIQI_contrast = max(local_contrast = sigma(9:15)(Bond_i)/sigma(1:8)(Bond_i))

tep_estimated: Number of edge pixels estimated
tep_sobel: Number of edge pixels counted using Sobel operator
Bond_i is the ith coefficient of the total 15 bands of 8×8 blocks of DCT coefficients. 
c1, c2, c3 are weighted coefficient

CQE_colorfulness = 0.02*log(stdev(alpha)^2/abs(mu(alpha))^0.2)*log(stdev(alpha)^2/abs(mu(alpha))^0.2)
