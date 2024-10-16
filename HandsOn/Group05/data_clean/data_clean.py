# -*- coding: utf-8 -*-
"""data_clean.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-qVQwLHlQs1UuP563UQW6Gncr6S46NcT
"""

## data cleaning script for handson

import pandas as pd

import os

path=os.getcwd()

path=path.replace('\\','/')

## Import 2 primary datasets
no2=pd.read_csv(path+'/20220408_NO2_Traffic.csv')
pm25=pd.read_csv(path+'/20220408_PM25_Traffic.csv')

## Upon inspection, main issue is that observations do not correspond to a single format (four measurements per row), there is no location provided
## and there are many unnecessary columns regarding date information,  background PM2.5 [ug/m^3] and background NO2 [ppb] are also an issue since
## they change depending on the location but are considered secondary measurements the two datasets can simply be combined using units as the differerentiating factor

pm25.head()

## Upon inspection, main issue is that observations do not correspond to a single format (four measurements per row), there is no location provided
## and there are many unnecessary columns regarding date information,  background PM2.5 [ug/m^3] and background NO2 [ppb] are also an issue since
## they change depending on the location but are considered secondary measurements the two datasets can simply be combined using units as the differerentiating factor

no2.head()

## check if data is missing in any column
no2[no2.isnull().all(1)]

## None found

## check if data is missing in any column
pm25[pm25.isnull().all(1)]

## Iterate through which columns we want to pivot from wide format to long format
## First we define a new column with the units used
columns_to_change_pm25=['Iowa PM2.5 [ug/m^3]','Chicago PM2.5 [ug/m^3]','Cranford PM2.5 [ug/m^3]', 'Magnolia PM2.5 [ug/m^3]']

columns_to_change_no2=['Iowa NO2 [ppb]','Chicago NO2 [ppb]','Cranford NO2 [ppb]', 'Magnolia NO2 [ppb]']


## Split info for background_element_measured (to be used as an id column)
pm25[['background_element_measured','background_units']]='PM2.5','ug/m^3'
pm25['background_observed']=pm25['Background PM2.5 [ug/m^3]']


no2[['background_element_measured','background_units']]='NO2','ppb'
no2['background_observed']=no2['Background NO2 [ppb]']

columns_to_preserve_no2=[]
columns_to_preserve_pm25=[]

## Add column to list for preservation

for a_column in no2.columns:
    if a_column not in columns_to_change:
        columns_to_preserve_no2.append(a_column)

for a_column in pm25.columns:
    if a_column not in columns_to_change:
        columns_to_preserve_pm25.append(a_column)


## Finally we apply pd.melt to each dataset and give a new name to our new columns (columns that need to be changed are defined by index)
no2=pd.melt(no2,id_vars=columns_to_preserve_no2,value_vars=columns_to_change_no2,var_name='column_name',value_name='observed')
pm25=pd.melt(pm25,id_vars=columns_to_preserve_pm25,value_vars=columns_to_change_pm25,var_name='column_name',value_name='observed')


## Apply  split to  columns into Street, element_measured, and Units
no2[['street','element_measured','units']]=no2['column_name'].str.split(' ',expand=True)

pm25[['street','element_measured','units']]=pm25['column_name'].str.split(' ',expand=True)

## Remove [] from units
no2['units']=no2['units'].str.replace('[','').str.replace(']','')
pm25['units']=pm25['units'].str.replace('[','').str.replace(']','')


# Use pandas concat to put datasets together
master_df=pd.concat([no2,pm25])

## Add name_formatting to certain columns
master_df['datetime_america_los_angeles']=master_df['datetime-America/Los_Angeles']
master_df['wind_direction_degrees']=master_df['Wind Direction [degrees]']
master_df['far_bound_local_roadway_vehicles_per_mile']=master_df['Far-bound Local Roadway (#vehicles/mile)']
master_df['far_bound_highway_vehicles_per_mile']=master_df['Far-bound Highway (#vehicles/mile)']
master_df['near_bound_local_roadway_vehicles_per_mile']=master_df['Near-bound Local Roadway (#vehicles/mile)']
master_df['near_bound_highway_vehicles_per_mile']=master_df['Near-bound Highway (#vehicles/mile)']
master_df['temperature_celsius']=master_df['Temperature [degC]']
master_df['pressure_mbar']=master_df['Pressure [mbar]']
master_df['humidity_pct']=master_df['Humidity [%]']
master_df['wind_speed_mph']=master_df['Wind Speed [mph]']


## Enrich data with street latitude/longitude
streets=pd.read_csv('streets.csv')

master_df=master_df.merge(streets,on=['street'])



master_df=master_df[['datetime_america_los_angeles','temperature_celsius','pressure_mbar','humidity_pct','wind_speed_mph','wind_direction_degrees',
                     'far_bound_local_roadway_vehicles_per_mile',
                     'far_bound_highway_vehicles_per_mile',
                     'near_bound_local_roadway_vehicles_per_mile',
                      'near_bound_highway_vehicles_per_mile','background_observed','background_element_measured','background_units','observed','street',
                     'element_measured','units','latitude','longitude']]

master_df.to_csv(path+'/updated.csv',index=False)