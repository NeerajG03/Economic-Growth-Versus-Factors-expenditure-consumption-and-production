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
energy_length = energy_data.Year >=1990
energy_data = energy_data[energy_length]
meat_data = meat_data.drop(['Entity', 'GDP ','Population', 'Continent'],axis =1)
meat_length = meat_data.Year >=1990
meat_data = meat_data[meat_length]
health_data = health_data.drop(['Entity','Population', 'Continent'],axis =1)
health_length = health_data.Year >=1990
health_data =health_data[health_length]


#MERGING ALL 3 DATASETs
data = pd.merge(pd.merge(energy_data , meat_data, on=['Code', 'Year']), health_data , on=['Code' , 'Year'])

#for training purpose select USA and check correlation between GDP and different caategories
data =data.loc[data['Code'].isin(['USA'])]

# replacing the NaN value of different attributes
data =data.fillna({                 # Since there is no starting value for health expenditure, replace NaN value with mean
    'health_expenditure':data['health_expenditure'].mean(),  
    'Meat_quantity':data['Meat_quantity'].mean(),
    'Energy_use ':data['Energy_use '].mean()
})
# automatic filling of na values with the middle or average values between two points for rest of the data
data = data.interpolate()   

#checking the null values
print(data)    

x = data.loc[:,"Energy_use "]         #0.62 -> moderately correlated
y = data.loc[:,"Meat_quantity"]         #0.275 -> Weakly  correlated
z = data.loc[:,"health_expenditure"]    #0.512 ->strongly correlated
g = data.loc[:,"GDP "]        
print(np.corrcoef(z,g))

