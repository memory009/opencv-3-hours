import pylab as plt 
import pandas as pd

data = pd.read_excel('test.xls')


x = data.iloc[0:,0]
y = data.iloc[0:,1]



plt.plot(x,y)
plt.show()
