#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 12:57:31 2020

@author: rojeen
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from matplotlib import cm

def visualize_3d(df, lin_reg_weights=[1,1,1], feat1=0, feat2=1, labels=2,
                 xlim=(-1, 1), ylim=(-1, 1), zlim=(0, 3),
                 alpha=0., xlabel='age', ylabel='weight', zlabel='height',
                 title=''):
    """ 
    3D surface plot. 
    Main args:
      - df: dataframe with feat1, feat2, and labels
      - feat1: int/string column name of first feature
      - feat2: int/string column name of second feature
      - labels: int/string column name of labels
      - lin_reg_weights: [b_0, b_1 , b_2] list of float weights in order
    Optional args:
      - x,y,zlim: axes boundaries. Default to -1 to 1 normalized feature values.
      - alpha: step size of this model, for title only
      - x,y,z labels: for display only
      - title: title of plot
    """

    # Setup 3D figure
    ax = plt.figure().gca(projection='3d')
    #plt.hold(True)

    # Add scatter plot
    ax.scatter(df[feat1], df[feat2], df[labels])

    # Set axes spacings for age, weight, height
    axes1 = np.arange(xlim[0], xlim[1], step=.05)  # age
    axes2 = np.arange(xlim[0], ylim[1], step=.05)  # weight
    axes1, axes2 = np.meshgrid(axes1, axes2)
    axes3 = np.array( [lin_reg_weights[0] +
                       lin_reg_weights[1]*f1 +
                       lin_reg_weights[2]*f2  # height
                       for f1, f2 in zip(axes1, axes2)] )
    plane = ax.plot_surface(axes1, axes2, axes3, cmap=cm.Spectral,
                            antialiased=False, rstride=1, cstride=1)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_xlim3d(xlim)
    ax.set_ylim3d(ylim)
    ax.set_zlim3d(zlim)

    if title == '':
        title = 'LinReg Height with Alpha %f' % alpha
    ax.set_title(title)

    plt.show()


def prepare_matrix(data):
    
    # add vector column for the intercept (initialized to be all 1.0) at the front of the matrix
    intercept_vector_column = [1.0 for i in range(0, len(data))]    
    data.insert(0, 'intercept', intercept_vector_column)
    
    # Scale each feature (age and weight) by its stdev so each scaled feature has a mean of 0    
    feat1_mean = np.mean(data[0].values)
    feat1_stdev = np.std(data[0].values)
    
    feat2_mean = np.mean(data[1].values)
    feat2_stdev = np.std(data[1].values)
    
    
    # Scale items in feature1 column
    for i in range(len(data)):
        data[0][i] = (data[0][i] - feat1_mean)/feat1_stdev
    
    # Scale items feature2 column
    for i in range(len(data)):
        data[1][i] = (data[1][i] - feat2_mean)/feat2_stdev
        
    return data

def linear_reg(scaled_data, alpha, num_iterations):
    
    # Initialize betas to 0    
    betas = [0 for i in range(len(scaled_data.columns)-1)]
    n = len(scaled_data)
    
    for iteration in range(num_iterations):
            
        # for each example in the dataset, find predicted height (add to predictions list)
        predictions = []
        for i in range(n):
            prediction = betas[0] + np.dot(betas[1:], [scaled_data[0][i], scaled_data[1][i]])
            predictions.append(prediction)
        
        '''
        To find empirical risk of predictions:
            
        For all examples,
            Subtract the actual value from the prediction
            Square these differences
            Sum up all of these squared differences
            Multiply the sum by 1/(2n)
        '''
        # Subtract the actual value from the prediction
        error_vector = np.subtract(np.asarray(predictions), scaled_data[2])
        
        # Square these differences
        squared_error_vector = np.square(error_vector)
        
        # Sum up all of these squared differences and multiply the sum by 1/(2n)
        empirical_risk = (1/(2*n)) * np.sum(squared_error_vector)
                
        # Update all of the betas        
        betas[0] = betas[0] - alpha*(1/n) * np.sum(error_vector*scaled_data['intercept'])
        
        for j in range(1, len(betas)): # takes on values 0 and 1 AKA [0,2)
            feature_vector = scaled_data[j-1].values
            betas[j] = betas[j] - alpha*(1/n) * np.sum(error_vector*feature_vector)

    return betas, empirical_risk       
        
                    

if __name__ == "__main__":
    # Import input1.csv, without headers for easier indexing
    inputCSV = sys.argv[1]
    outputCSV = sys.argv[2]
    
    # Learning rates
    alphas = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
    
    num_iterations = 100
    
    ideal_alpha = 1
    
    ideal_iterations = 90
   
    # Import input1.csv, without headers for easier indexing
    data = pd.read_csv(inputCSV, header=None)   
        
    scaled_data = prepare_matrix(data)
    
    outFile = open(outputCSV, "w")
       
    for alpha in alphas:
        betas, empirical_risk = linear_reg(scaled_data, alpha, num_iterations)
        
        visualize_3d(data, lin_reg_weights=betas)
    
        line = "{},{},{},{},{}\n".format(alpha, num_iterations, betas[0], betas[1], betas[2])
    
        outFile.write(line)
    
    ideal_betas, ideal_empirical_risk = linear_reg(scaled_data, ideal_alpha, ideal_iterations)
    
    ideal_line = "{},{},{},{},{}".format(ideal_alpha, ideal_iterations, ideal_betas[0], ideal_betas[1], ideal_betas[2])
    
    visualize_3d(data, lin_reg_weights=ideal_betas)
    
    outFile.write(ideal_line)
    outFile.close()