#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 20:34:15 2020

@author: rojeen
"""
import sys
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
'''
Perceptron Algorithm

Input: A set of examples, (x1, y1), ··· , (xn, yn)
Output: A perceptron defined by (w0, w1, ··· , wd)

Begin
2. Initialize the weights wj to 0 8j 2 {0, ··· , d}
3. Repeat until convergence
4. For each example xi 8i 2 {1, ··· , n}
5. if yif(xi)  0 #an error?
6. update all wj with wj := wj +yixij #adjust the weights

End

'''

def visualize_scatter(df, feat1=0, feat2=1, labels=2, weights=[-1, -1, 1],
                      title=''):
    """
        Scatter plot feat1 vs feat2.
        Assumes +/- binary labels.
        Plots first and second columns by default.
        Args:
          - df: dataframe with feat1, feat2, and labels
          - feat1: column name of first feature
          - feat2: column name of second feature
          - labels: column name of labels
          - weights: [w1, w2, b] 
    """

    # Draw color-coded scatter plot
    colors = pd.Series(['r' if label > 0 else 'b' for label in df[labels]])
    ax = df.plot(x=feat1, y=feat2, kind='scatter', c=colors)

    # Get scatter plot boundaries to define line boundaries
    xmin, xmax = ax.get_xlim()

    # Compute and draw line. ax + by + c = 0  =>  y = -a/b*x - c/b
    a = weights[0]
    b = weights[1]
    c = weights[2]

    def y(x):
        return (-a/b)*x - c/b

    line_start = (xmin, xmax)
    line_end = (y(xmin), y(xmax))
    line = mlines.Line2D(line_start, line_end, color='red')
    ax.add_line(line)


    if title == '':
        title = 'Scatter of feature %s vs %s' %(str(feat1), str(feat2))
    ax.set_title(title)

    plt.show()


def sign_step_function(example, weights):
    # dot product of the weights of the features + the bias (basically add the weighted features and the bias) 
    # return 1 if positive, -1 if negative
    return -1 if (np.dot(example[:-1], weights[:-1]) + weights[-1]*1) < 0 else 1

def perceptron_learning(data):

    data_list = data.values
    #print(data_list)
    # Input: A set of examples, (featureA(1), featureB(1), label1), ··· , (featureA(n), featureB(n), labeln)
    
    # Initialize the weights to 0: [0,0,0]
    weights = [0 for i in range(0, len(data.columns))]
    #print(weights)
    output_list = []

    # i = row number
    # j = feature number (0, 1, 2)
    # specific element = data[column][row]
    
    # while the weights are still changing (while not converging)
    while True:
        # For each example xi for all i in {1, ··· , n} where n = number of rows
        # for each example (each row), in data1.csv it will be [0, 17)
        for i in range(len(data)):
            
            #print('i: ' + str(i))
            
            # get correct label: y_i (get last element, from the example: label)
            correct_label = data_list[i][-1]
            
            # get predicted label: f(x_i)
            # predicted_label = sign(column at that row, weights)
            predicted_label = sign_step_function(data_list[i], weights)
            
            #print("correct_label: " + str(correct_label) + " predicted_label: " + str(predicted_label))
            
            #if y_i * f(x_i) <= 0
            if (correct_label * predicted_label) <= 0:
                #print("label not correct so update weights")
                
                # update all w_j with w_j = w_j + y_i * x_(ij)
                for j in range(len(data.columns)-1):
                    weights[j] += correct_label * data_list[i][j]
                
                weights[-1] += correct_label * 1
                
        if (weights in output_list):
            output_list.append(weights.copy())
            break
        output_list.append(weights.copy())
        
                
    output_df = pd.DataFrame.from_records(output_list)
    
    #visualize_scatter(output_df, 0, 1, 2, weights, title='')
    
    return output_df, weights

if __name__ == "__main__":
    # Import input1.csv, without headers for easier indexing
    inputCSV = sys.argv[1]
    outputCSV = sys.argv[2]
   
    # Import input1.csv, without headers for easier indexing
    data = pd.read_csv(inputCSV, header=None)
            
    output_df, out_weights = perceptron_learning(data)
    output_df.to_csv(outputCSV, header=False, index=False) 
    
    #visualize_scatter(data, weights = out_weights)
