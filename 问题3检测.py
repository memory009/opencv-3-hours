import pylab as plt 
import pandas as pd


data = pd.read_excel('Resources\EdgeContour1.xls')
data2 = pd.read_excel('Resources\EdgeContour2.xls')

x = data.iloc[0:,0]
y = data.iloc[0:,1]

x2 = data2.iloc[0:,0]
y2 = data2.iloc[0:,1]

# plt.plot(x,y,x2,y2,data=None)
plt.axis('off')  #去掉坐标轴
plt.plot(x,y,data=None,color='black')
plt.plot(x2,y2,data=None,color='black')
# plt.savefig(fname="调整.png")
plt.show()



