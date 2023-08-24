# -*- coding: utf-8 -*-
"""Gas Turbine.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A8ZkiN7TN3zzBXQ5fQJSITt_dqZzCaMr
"""

from google.colab import files
uploaded = files.upload()

# Supress Warnings
import warnings
warnings.filterwarnings('ignore')

#Importing Libraries
import pandas as pd
import numpy as np

#Importing Dataset
turbine=pd.read_csv("/content/gas_turbines.csv")
turbine

"""Data Exploration"""

turbine.isnull().sum()

"""Descriptive Analysis"""

turbine.shape

#Checking the data types
turbine.dtypes

#Unique values for every feature
turbine.nunique()

turbine.info()

turbine.describe()

turbine.duplicated().sum()

numerical_features = turbine.describe(include=["int64","float64"]).columns
numerical_features

"""Data Visualization"""

#Importing Libraries seaborn and matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Having a look at the correlation matrix

plt.figure(figsize=(16,12))
mask = np.zeros_like(turbine.corr(), dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(data=turbine.corr(), cmap="jet", annot=True,linewidths=1, linecolor='white',mask=mask)

numerical_features=[feature for feature in turbine.columns if turbine[feature].dtypes != 'O']
for feat in numerical_features:
    skew = turbine[feat].skew()
    sns.distplot(turbine[feat], kde= False, label='Skew = %.3f' %(skew), bins=30)
    plt.legend(loc='best')
    plt.show()

#boxplot
ot=turbine.copy()
fig, axes=plt.subplots(11,1,figsize=(14,16),sharex=False,sharey=False)
sns.boxplot(x='AT',data=ot,palette='crest',ax=axes[0])
sns.boxplot(x='AP',data=ot,palette='crest',ax=axes[1])
sns.boxplot(x='AH',data=ot,palette='crest',ax=axes[2])
sns.boxplot(x='AFDP',data=ot,palette='crest',ax=axes[3])
sns.boxplot(x='GTEP',data=ot,palette='crest',ax=axes[4])
sns.boxplot(x='TIT',data=ot,palette='crest',ax=axes[5])
sns.boxplot(x='TAT',data=ot,palette='crest',ax=axes[6])
sns.boxplot(x='TEY',data=ot,palette='crest',ax=axes[7])
sns.boxplot(x='CDP',data=ot,palette='crest',ax=axes[8])
sns.boxplot(x='CO',data=ot,palette='crest',ax=axes[9])
sns.boxplot(x='NOX',data=ot,palette='crest',ax=axes[10])
plt.tight_layout(pad=2.0)

"""Multivariate Analysis"""

for i in turbine.columns:
    if i!="TEY":
        plt.scatter(np.log(turbine[i]), np.log(turbine['TEY']))
        plt.title(i+ ' vs TEY')
        plt.grid()
        plt.show()

x = turbine.drop('TEY', axis=1)
y = turbine[["TEY"]]

"""Feature Selection Technique"""

model_data = turbine[['CDP', 'GTEP','TIT', 'TAT', 'AFDP', 'CO', 'AT',"TEY"]]
model_data.head()

"""Data Pre-Processing"""

continuous_feature=[feature for feature in model_data.columns if model_data[feature].dtype!='O']
print('Continuous Feature Count {}'.format(len(continuous_feature)))

from sklearn.preprocessing import StandardScaler

df_scaled = model_data.copy()
features = df_scaled

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df_scaler= scaler.fit_transform(features.values)
df_scaled = pd.DataFrame(df_scaler, columns=features.columns)
df_scaled

"""Test Train Split With Imbalanced Dataset"""

x = df_scaled.drop('TEY',axis=1)
y = df_scaled[['TEY']]

from sklearn.model_selection import train_test_split

# Splitting data into test data and train data

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=3)

import keras
from keras.models import Sequential
from keras.layers import Dense
import keras
keras. __version__

model_data
#assigning predictor variables to x and response variable to y
x = model_data.drop('TEY', axis=1)
y = model_data[["TEY"]]

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.20, random_state=42)

scaler_train = StandardScaler()
scaler_test = StandardScaler()

x_train_scaled = scaler_train.fit_transform(x_train) # scaling train data -- predictor
x_test_scaled  = scaler_test.fit_transform(x_test) # scaling test data -- predictor

print(x_train_scaled.shape)
print(x_test_scaled.shape)
print(y_train.shape)
print(y_test.shape)

# since we have continuous ouput, AF is not required in the o/p layer
model = Sequential()
model.add( Dense( units = 50 , activation = 'relu' , kernel_initializer = 'normal', input_dim = 7)) # input layer
model.add( Dense( units = 20 , activation = 'tanh' , kernel_initializer = 'normal' )) # hidden layer
model.add( Dense( units = 1  , kernel_initializer = 'normal' )) # o/p layer

model.compile(optimizer= "adam", loss="mse", metrics= ["mae", "mse"])
model.fit(x_train_scaled, y_train , batch_size=50, validation_split=0.3, epochs=100,  verbose=1)

plt.figure(figsize=(16,9))
plt.plot(model.history.history['mae'])
plt.plot(model.history.history['mse'])
plt.title("Model's Mean Absolute and Squared Errors")
plt.xlabel('Epoch')
plt.ylabel('Error')
plt.legend(['Mean Absulote Erroe', 'Mean Squared Error'],loc = 'upper left')
plt.show()
#summarize history for loss
plt.figure(figsize=(16,9))
plt.plot(model.history.history['loss'])
plt.plot(model.history.history['val_loss'])
plt.title('Model-loss')
plt.xlabel('Epoch')
plt.ylabel('Mean-Absolute-Error')
plt.legend(['Training Error', 'Testing Error'],loc='upper left')
plt.show()

"""Predicting values from Model using same dataset"""

# generating predictions for test data
y_predict_test = model.predict(x_test_scaled)

# creating table with test price & predicted price for test
predictions_df = pd.DataFrame(x_test)
predictions_df['Actual'] = y_test
predictions_df['Predicted'] = y_predict_test
print(predictions_df.shape)
predictions_df.head(10)

# Computing the absolute percent error
APE=100*(abs(predictions_df['Actual']-predictions_df['Predicted'])/predictions_df['Actual'])
print('The Accuracy for Test Data -- ANN model = ', 100-np.mean(APE))

# adding absolute percent error to table
predictions_df['APE %']=APE
predictions_df.head()

"""Residual Analysis"""

plt.figure(figsize=(12,10))
sns.distplot(y_test-y_predict_test,bins=50)

predictions_df['Error'] = (predictions_df['Actual'] - predictions_df['Predicted'])/(predictions_df['Actual'])
predictions_df.reset_index(drop = True)

#Residuals values  = y - yhat
import statsmodels.api as smf
smf.qqplot(predictions_df['Error'], line = 'q')
plt.title('Normal Q-Q plot of residuals')
plt.show()