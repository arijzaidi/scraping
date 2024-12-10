import pandas  as pd
from pandas import read_csv
import matplotlib.pyplot as plt 
import seaborn as sns

df=read_csv('data/cars.csv')

df['Prix'] = pd.to_numeric(df['Prix'].str.replace(' ', ''), errors='coerce')

price=df['Prix']
marque=df['Marque']
print(df.groupby('Marque')) 
plt.scatter(marque,price)
plt.show()

