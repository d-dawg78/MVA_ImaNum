#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 09:46:28 2020

@author: Antoine1
"""

import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

#imgpil=Image.open("10_img_.png")
#img=np.array(imgpil)/255

#img = mpimg.imread("image.jpg")
#img=plt.imread('image2.png')

def tr_gamma(img,gamma):
    img_2=np.zeros(img.shape)
    
 
    for m in range(img.shape[0]):
        for n in range(img.shape[1]):
            for j in range(3):
                img_2[m,n,j]=img[m,n,j]
                if img[m,n,j]>1:
                    img_2[m,n,j]=1
                if img[m,n,j]<0:
                    img_2[m,n,j]=0            
                img_2[m,n,j]=img_2[m,n,j]**(1/gamma) 
    return img_2
    
def linear_transform(img,T):
    img_out=np.zeros(img.shape)
    
 
    for m in range(img.shape[0]):
        for n in range(img.shape[1]):
            img_out[m,n,:]=np.dot(T,img[m,n,:].T).T
            
    return img_out

def correction(img):
    avg=np.zeros(3)
    
    avg[1]=np.median(img[:,:,1])
    avg[2]=np.median(img[:,:,2])
    

    print('avg : ', avg)
    
    wc1=np.min(img[:,:,0])+pct*(np.max(img[:,:,0])-np.min(img[:,:,0]))
    wc2=np.max(img[:,:,0])-pct*(np.max(img[:,:,0])-np.min(img[:,:,0]))
    a=(np.max(img[:,:,0])-np.min(img[:,:,0]))/(wc2-wc1)
    b=np.min(img[:,:,0])-a*wc1


    
    img_cor=np.zeros(img.shape)
    for m in range(img.shape[0]):
        for n in range(img.shape[1]):
            #for j in range(3):
            
            img_cor[m,n,1]=img[m,n,1]-avg[1]
            img_cor[m,n,2]=img[m,n,2]-avg[2]
            if img[m,n,0]<wc1:
                img[m,n,0]=wc1
            if img[m,n,0]>wc2:
                img[m,n,0]=wc2
            img_cor[m,n,0]=a*img[m,n,0]+b
                
            
    return img_cor
                
def log_lms(img):
   img_log=np.zeros(img.shape)
   for m in range(img.shape[0]):
        for n in range(img.shape[1]):
            for j in range(3):
                if img[m,n,j]<eps:
                    img[m,n,j]=eps
                img_log[m,n,j]=np.log(img[m,n,j])
   return img_log

def log_lms_inv(img):
   img_log_inv=np.zeros(img.shape)
   for m in range(img.shape[0]):
        for n in range(img.shape[1]):
            for j in range(3):
                img_log_inv[m,n,j]=10**(img[m,n,j])
   return img_log_inv

def plot_histo_luminance(img_lab):
    histo,bins=np.histogram(img_lab[:,:,0].reshape(img.shape[0],img.shape[1]),bins=256)
    x=np.linspace(np.min(img_lab[:,:,0]),np.max(img_lab[:,:,0]),256)
    plt.plot(x,histo)

T_XYZ=np.array([[0.5141,0.3239,0.1604],
               [0.2651,0.6702,0.0641],
               [0.0241,0.1228,0.8444]])

T_lms=np.array([[0.3897,0.6890,-0.0787],
               [-0.2298,1.1834,0.0464],
               [0.0000,0.0000,1.0000]])
T1=np.array([[1/np.sqrt(3),0,0],
               [0,1/np.sqrt(6),0],
               [0,0,1/np.sqrt(2)]])

T2=np.array([[1,1,1],
               [1,1,-2],
               [1,-1,0]])
T_pca=np.dot(T1,T2)

#list_path=["profil_foret","image1","image2","605","627","643","3027","3087","7291","9602","13252","15738"]
#list_path=["seathru1_orig","seathru2_orig","seathru3_orig"]
list_path=["seathru4_orig"]


for path in list_path:
    img=plt.imread('test/'+ path +".png")
    img=np.array(img)
    
    
    if img.shape[2]==4:
        img=img[:,:,0:3]
        #print(img.shape)
        
    pct=0.05
    gamma=0.44
    eps=0.005
    
    
    img_gamma=tr_gamma(img,gamma)
    img_XYZ=linear_transform(img, T_XYZ)
    img_lms=linear_transform(img_XYZ, T_lms)
    img_log_lms=log_lms(img_lms)
    img_lab=linear_transform(img_log_lms, T_pca)
    
    img_cor_lab=correction(img_lab)
    
    img_cor=linear_transform(img_cor_lab, np.linalg.inv(T_pca))
    img_log_inv=log_lms_inv(img_cor)
    img_lms_inv=linear_transform(img_log_inv, np.linalg.inv(T_lms))
    img_xyz_inv=linear_transform(img_lms_inv, np.linalg.inv(T_XYZ))
    #img_out=img_xyz_inv
    img_out=tr_gamma(img_xyz_inv, 1/gamma)
    plt.imsave("out2/out"+path+".png",img_out)
    
    
    # print('min : ', np.min(img_out))
    # print('max : ', np.max(img_out))
    
    # plt.figure()
    # plt.subplot(211)
    # plt.imshow(img)
    # plt.subplot(212)
    # plt.imshow(img_out)
    
    # plt.figure()
    # plot_histo_luminance(img_lab)
    # plot_histo_luminance(img_cor_lab)
    
    # plt.figure()
    # plt.plot(img_lab[:,:,1].reshape(img.shape[0]*img.shape[1]),img_lab[:,:,2].reshape(img.shape[0]*img.shape[1]),'.')
    
