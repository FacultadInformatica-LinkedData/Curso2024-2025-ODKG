# %%
## data cleaning script for handson


import pandas as pd

import os

path=os.getcwd()

path=path.replace('\\','/')

## Import 2 primary datasets
no2=pd.read_csv(path+'/20220408_NO2_Traffic.csv')
pm25=pd.read_csv(path+'/20220408_PM25_Traffic.csv')


## create column ids uniquely iding each observation to a dataset

no2['dataset_id']=1
pm25['dataset_id']=2

# %%

## Upon inspection, main issue is that observations do not correspond to a single format (four measurements per row), there is no location provided
## and there are many unnecessary columns regarding date information, 
## background PM2.5 [ug/m^3] and background NO2 [ppb] are also an issue since they change depending on the location but are considered secondary measurements
#the two datasets can simply be combined using units as the differerentiating factor


pm25.head()



# %%

## Upon inspection, main issue is that observations do not correspond to a single format (four measurements per row), there is no location provided
## and there are many unnecessary columns regarding date information, 
## background PM2.5 [ug/m^3] and background NO2 [ppb] are also an issue since they change depending on the location but are considered secondary measurements
#the two datasets can simply be combined using units as the differerentiating factor


no2.head()



# %%
## check if data is missing in any column 

no2[no2.isnull().all(1)]

## None found

# %%
## check if data is missing in any column
pm25[pm25.isnull().all(1)]

# %%
## check data length
len(pm25)

# %%
## check data length
len(no2)

# %%
## check join conditions for performing a join
pm_25_datetimes=pm25['datetime-America/Los_Angeles'].tolist()

for a_datetime in no2['datetime-America/Los_Angeles']:
    if (a_datetime in pm_25_datetimes):
        print(a_datetime)

## since datasets share disjoint points in time, a union is better

# %%
test_join=pd.concat([pm25,no2])

test_join.head()

# %%
## Iterate through which columns we want to pivot from wide format to long format

## first we define columns to be used  (with proper formatting)

columns_to_change=['Iowa NO2_ppb','Chicago NO2_ppb','Cranford NO2_ppb','Magnolia NO2_ppb','Iowa PM2.5_ug/m^3','Chicago PM2.5_ug/m^3',
                   'Cranford PM2.5_ug/m^3','Magnolia PM2.5_ug/m^3','Riverside backgroundPM2.5_ug/m^3','Riverside backgroundNO2_ppb',
                  'Riverside windDirection_degrees','Riverside farBoundLocalRoadway_#VehiclesPerMile','Riverside farBoundHighwayVehicles_#VehiclesPerMile',
                 'Riverside nearBoundLocalRoadwayVehicles_#VehiclesPerMile','Riverside nearBoundHighwayVehicles_#VehiclesPerMile','Riverside temperature_celsius',
                 'Riverside pressure_mbar','Riverside humidity_pct','Riverside windSpeed_mph']




## union datasets

df=pd.concat([no2,pm25])

## reformat names of columns so that they are all consistent
df['Iowa NO2_ppb']=df['Iowa NO2 [ppb]']
df['Chicago NO2_ppb']=df['Chicago NO2 [ppb]']
df['Cranford NO2_ppb']=df['Cranford NO2 [ppb]']
df['Magnolia NO2_ppb']=df['Magnolia NO2 [ppb]']
df['Riverside backgroundNO2_ppb']=df['Background NO2 [ppb]']


df['Iowa PM2.5_ug/m^3']=df['Iowa PM2.5 [ug/m^3]']
df['Chicago PM2.5_ug/m^3']=df['Chicago PM2.5 [ug/m^3]']
df['Cranford PM2.5_ug/m^3']=df['Cranford PM2.5 [ug/m^3]']
df['Magnolia PM2.5_ug/m^3']=df['Magnolia PM2.5 [ug/m^3]']
df['Riverside backgroundPM2.5_ug/m^3']=df['Background PM2.5 [ug/m^3]']


df['datetime_america_los_angeles']=df['datetime-America/Los_Angeles']
df['Riverside windDirection_degrees']=df['Wind Direction [degrees]']

df['Riverside farBoundLocalRoadway_#VehiclesPerMile']=df['Far-bound Local Roadway (#vehicles/mile)']
df['Riverside farBoundHighwayVehicles_#VehiclesPerMile']=df['Far-bound Highway (#vehicles/mile)']
df['Riverside nearBoundLocalRoadwayVehicles_#VehiclesPerMile']=df['Near-bound Local Roadway (#vehicles/mile)']
df['Riverside nearBoundHighwayVehicles_#VehiclesPerMile']=df['Near-bound Highway (#vehicles/mile)']
df['Riverside temperature_celsius']=df['Temperature [degC]']
df['Riverside pressure_mbar']=df['Pressure [mbar]']
df['Riverside humidity_pct']=df['Humidity [%]']
df['Riverside windSpeed_mph']=df['Wind Speed [mph]']

columns_to_keep=['datetime_america_los_angeles','observation_id']



all_cols=[]

for a_col in columns_to_change:
    all_cols.append(a_col)

for a_col in columns_to_keep:
    all_cols.append(a_col)


## apply pd.melt to  (with column name of element_units format)
df=pd.melt(df[all_cols],id_vars=columns_to_keep,value_vars=columns_to_change,var_name='column_name',value_name='observed')



## apply  split to  columns and get street
df[['location','element_units']]=df['column_name'].str.split(' ',expand=True)

df[['element','units']]=df['element_units'].str.split('_',expand=True)



print(df.head())




locations=pd.read_csv('locations.csv')


df=df.merge(locations,on=['location'])


## remove null values inherited from union
df=df[(~df['observed'].isna()) & (df['observed']!=-999999)]

## because many background elements are shared between the two datasets, we employe drop_duplicates()

df['observation_id']=df.index

df[['datetime_america_los_angeles','dataset_id','observation_id','element','units','observed','location','city','county','state','country','latitude','longitude']].to_csv('riverside_pollution_study.csv',index=False)







# %%


# %%
no2.to_csv(path+'/no2.csv',index=False)

# %%


# %%
