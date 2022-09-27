import pandas as pd
import numpy as np
#LOADING THE DATASET
missing_values =["N/a", "na", np.nan, "", 0, "NaN"]
energy_data = pd.read_csv("energy-use-per-capita-vs-gdp-per-capita.csv",na_values = missing_values)
meat_data =pd.read_csv("meat-consumption-vs-gdp-per-capita.csv", na_values = missing_values)
health_data =pd.read_csv("healthcare-expenditure-vs-gdp.csv",na_values = missing_values)

#CEANING THE DATASET

#extracting the data between 1990 -2020 and droping the redundant columns
energy_data = energy_data.drop(['GDP ','Population', 'Continent'],axis =1)
energy_data = energy_data[energy_data.Year >=1990]
meat_data = meat_data.drop(['Entity', 'GDP ','Population', 'Continent'],axis =1)
meat_data = meat_data[meat_data.Year >=1990]
health_data = health_data.drop(['Entity','Population', 'Continent'],axis =1)
health_data =health_data[health_data.Year >=1990]


#MERGING ALL 3 DATASETs
data = pd.merge(pd.merge(energy_data , meat_data, on=['Code', 'Year']), health_data , on=['Code' , 'Year'])

#for training purpose select USA and check correlation between GDP and different caategories
data =data.loc[data['Code'].isin(["USA"])]             # add countries of your choice. 

# automatic filling of na values with ffill and bfill values between two points grouped by country for rest of the data
# data = data.interpolate()   
data["Meat_quantity"] = data.groupby('Entity')['Meat_quantity'].transform(lambda x: x.ffill().bfill())
data["Energy_use "] = data.groupby('Entity')['Energy_use '].transform(lambda x: x.ffill().bfill())
data["health_expenditure"] = data.groupby('Entity')['health_expenditure'].transform(lambda x: x.ffill().bfill())
data["GDP "] = data.groupby('Entity')['GDP '].transform(lambda x: x.ffill().bfill())



with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 6,
                       ):
                            print(data)

#checking the null values
# print(data.isnull().sum())

x = data.loc[:,"Energy_use "]         #0.62 -> moderately correlated
y = data.loc[:,"Meat_quantity"]         #0.275 -> Weakly  correlated
z = data.loc[:,"health_expenditure"]    #0.97 ->strongly correlated
g = data.loc[:,"GDP "]        
print(np.corrcoef(y,g))

