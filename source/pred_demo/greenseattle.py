# Standard import libraries
import matplotlib
import numpy as np

import pandas as pd
import pickle

# Greening Seattle libraries
# to import
# from Prediction_function import Predict_function_Normalization
from matplotlib import pyplot as plt
matplotlib.rcParams.update({'font.size': 20})


def prepare_nn():
    """
    return trained features and associated weights for nn
    """
    # dataset0 = pd.read_csv('all_data.csv', encoding='latin-1')
    # features
    # features_select = ['Total_Population', 'Pop_fraction',
    #                    'RACK_CAPACITY', 'Miles_Bike_Lanes']
    # name of label
    # label_select = ['AAWDT']
    # Normlized the data
    # Note the the prediction should use the same Normlization
    # dataset = dataset0/dataset0.mean()
    # train_dataset = dataset.sample(frac=0.8, random_state=0)
    # test_dataset = dataset.drop(train_dataset.index)

    # train_features = train_dataset[features_select]
    # test_features = test_dataset[features_select]

    # train_labels = train_dataset[label_select]
    # test_labels = test_dataset[label_select]

    f = open('Weights_MultiFeatures.pckl', 'rb')
    [W1, b1, W2, b2, W3, b3] = pickle.load(f)
    f.close()

    return W1, b1, W2, b2, W3, b3


def feature_projection(feature, zipcode):
    """
    use trained features and associated weights for nn
    to predict future traffic
    """
    # features
    features_select = ['Total_Population', 'Pop_fraction',
                       'RACK_CAPACITY', 'Miles_Bike_Lanes']
    # name of label
    label_select = ['AAWDT']

    dataset0 = pd.read_csv('all_data.csv', encoding='latin-1')
    zip_data = dataset0.loc[dataset0['ZIPCODE'] == zipcode]

    W1, b1, W2, b2, W3, b3 = prepare_nn()

    feature0 = zip_data.max()[features_select]

    list_proportion = np.arange(0, 10, 0.5)
    feature_idx = feature
    list_prediction = []
    Norm_mean = dataset0.mean()[features_select]
    Norm_std = dataset0.std()[features_select]
    label_mean = dataset0.mean()[label_select]
    # label_std = dataset0.std()[label_select]

    for proportion in list_proportion:
        feature_test = feature0.copy()
        feature_test[feature_idx] = feature0[feature_idx]*proportion
        Label_test = \
            Predict_function_Normalization(feature_test,
                                           Norm_mean, Norm_std,
                                           W1, b1, W2, b2, W3, b3)
        list_prediction.append(Label_test*label_mean)

    output_list = []
    for i in range(0, np.size(list_proportion)):
        output_list.append(list_prediction[i][0])

    return output_list


def model_viz(zipcode):
    """
    For model visualization
    """
    # dataset0 = pd.read_csv('all_data.csv',encoding='latin-1')
    list_proportion = np.arange(0, 10, 0.5)

    pop_val = feature_projection(0, zipcode)
    rack_val = feature_projection(2, zipcode)
    lanes_val = feature_projection(3, zipcode)

    zipcode_identifier = zipcode*np.ones(np.size(pop_val))

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(list_proportion, np.log(pop_val),
            'o-', color='blue', label='Population')
    ax.plot(list_proportion, np.log(rack_val),
            'x-', color='red', label='Bike Rack Capacity')
    ax.plot(list_proportion, np.log(lanes_val),
            's-', color='green', label='Bike Lanes (ft)')

    plt.xlabel('Proportional changes')
    plt.ylabel('Log10 Traffic')
    plt.suptitle('Projected Traffic Change in Zipcode', fontsize=18)
    plt.xlim([-0.1, 10.5])
    plt.tight_layout
    plt.legend(loc='lower right', title_fontsize='xx-small')

    matrix = np.stack((np.log(pop_val), np.log(rack_val),
                      np.log(lanes_val), zipcode_identifier)).T

    return matrix


def Predict_function(Predict_input, W1, b1, W2, b2, W3, b3):
    '''
    The prediction function represented by neural network with tanh activation
    Predict_input is the data after normlization
    '''
    Predict_output = function_tanh(function_tanh(Predict_input@W1+b1)
                                   @ W2 + b2) @ W3 + b3
    return np.maximum(Predict_output, 0)


def Predict_function_Normalization(Predict_input, Norm_mean, Norm_std,
                                   W1, b1, W2, b2, W3, b3):
    '''
    The prediction function represented by neural network with tanh activation
    Predict_input is the raw data withour normlization
    Predict_df is the dataframe for prediction
    '''
    Predict_input = (Predict_input) / Norm_mean
    Predict_output = function_tanh(function_tanh(Predict_input@W1+b1)
                                   @ W2+b2)@W3+b3
    return np.maximum(Predict_output, 0)


def function_tanh(x):
    '''
    tanh activation function
    '''
    y = (2 / (1 + np.exp(-2 * x))) - 1
    return y


def convert_csv(*args):
    """
    An arbitrary function for activating travis
    Converts a an input csv file to a pandas dataframe
    Input-- filepath, string type
    Output-- returns a pandas dataframe

    """
    filepath = args[0]
    try:
        assert isinstance(filepath, str)
    except AssertionError:
        print('the input argument is a string for the filpath ' +
              'to the csv file')
    else:
        dframe = pd.read_csv(filepath)
        return dframe
