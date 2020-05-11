#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 18:57:28 2020

@author: rojeen
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from skimage import io
import os
'''
Algorithm:
    Initialize randomnly the 3 centers (mean_1, mean_2, mean_3)
    Repeat until convergence (no change in culsters OR maximum number of iterations reached:
        assign each point x_i to the cluster with the closest mean_j
        calculate the new mean for each cluster using mean = 1/(size of cluster) * (sum of all elements in the cluster)
'''

def create_image_array(filename):
    # Load tree image as ndarray from filename where RBG image is MxNx3 (RGB colorsin  3rd dimension)
    # Convert ndarray to numpy array of floats
    trees_img_arr = np.array(io.imread(filename), dtype=np.float64)
        
    # Normalize values in trees numpy array
    trees_img_arr /= 255
    
    # Get M, N, and RBG = 3 of the tree image array
    m = trees_img_arr.shape[0]
    n = trees_img_arr.shape[1]
    RGB = trees_img_arr.shape[2] # should be 3
        
    # Give new shape of array rows = M*N and columns = RGB = 3
    reshaped_tree_img_array = np.reshape(trees_img_arr, (m * n, RGB))
    
    return reshaped_tree_img_array, m, n

def run_k_means(reshaped_tree_img_array):
    # Seed random state in order to make randomness deterministic for random number generation for centroid initialization
    # Run fit (with parameter reshaped_tree_img_array which makes up the training instances to cluster) to compute k-means clustering
    k_means_out = KMeans(n_clusters=20, random_state=8).fit(reshaped_tree_img_array)
        
    # Predict the closest cluster each sample in reshaped_tree_img_array belongs to
    # cluster_labels = array with index of the cluster each sample belongs to
    cluster_labels = k_means_out.predict(reshaped_tree_img_array)
    
    return k_means_out, cluster_labels

def create_segmented_image(m, n, k_means_out, cluster_labels):
    # Start with first sample
    sample = 0
    
    # Initialize segmented_image with ones (shape MxNx3)
    segmented_image = np.ones((m, n, k_means_out.cluster_centers_.shape[1])) # MxNx3
    
    for i in range(np.shape(segmented_image)[0]): # rows
        for j in range(np.shape(segmented_image)[1]): # columns
            # set the pixel at i*j equal to the same RGB as the cluster it is closest to
            segmented_image[i][j] = k_means_out.cluster_centers_[cluster_labels[sample]]
            sample = sample + 1
    return segmented_image

def plot_segmented_image(segmented_image):
    plt.figure()
    plt.axis('off')
    plt.imshow(segmented_image)
    
def save_segmented_image_to_png_file(segmented_image):
    outfile = os.path.join(cwd, 'trees_segmented.png')
    io.imsave(outfile, segmented_image)

if __name__ == "__main__":
    
    # Get current working directory to locate the image file
    cwd = os.getcwd()
    
    # Get the filepath in the current working directory
    filename = os.path.join(cwd, 'trees.png')
    
    # Get the image array to be used in k-means
    reshaped_tree_img_array, m, n = create_image_array(filename)
    
    # Run k-means to get cluster_labels
    k_means_out, cluster_labels = run_k_means(reshaped_tree_img_array)
    
    # Get segmented image array
    segmented_image = create_segmented_image(m, n, k_means_out, cluster_labels)
    
    # Plot segmented image
    plot_segmented_image(segmented_image)
    
    # Save segmented image to png file

    #save_segmented_image_to_png_file(segmented_image)
    