from functions import *

df = pd.read_csv('../data/2019.12.06.csv')
df.head()


tp_avg = df.drop('tp', axis=1).mean(axis=1)
myDict = dict(zip(df['tp'], tp_avg))
pd.DataFrame(sorted(myDict.items(), key=lambda x: x[1])).iloc[-20:]


avg_avg = df.drop('tp', axis=1).mean(axis=0)
myDict = dict(zip(df.columns[1:], avg_avg))
pd.DataFrame(sorted(myDict.items(), key=lambda x: x[1])).iloc[-20:]
