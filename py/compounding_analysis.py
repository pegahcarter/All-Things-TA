from functions import *

df = pd.read_csv('../data/2019.12.06.csv')
df.head()


tp_avg = df.drop('tp', axis=1).mean(axis=1)
myDict = dict(zip(df['tp'], tp_avg))
pd.DataFrame(sorted(myDict.items(), key=lambda x: x[1])).iloc[-30:]

myDict = dict(df.iloc[144])
myDict.pop('tp')
pd.DataFrame(sorted(myDict.items(), key=lambda x: x[1])).iloc[-20:]


myDict = dict(zip(df['tp'], df['15-30-50']))
pd.DataFrame(sorted(myDict.items(), key=lambda x: x[1])).iloc[-30:-15]



avg_avg = df.drop('tp', axis=1).mean(axis=0)
myDict = dict(zip(df.columns[1:], avg_avg))
pd.DataFrame(sorted(myDict.items(), key=lambda x: x[1])).iloc[-35:-20]


''' TO - DO
1. Adjust ATTA
    - 21-30-55
    - Only 2 TP's in signal messages
    - 5% Tp1, 95% Tp2
2. Adjust WC
    - 15-30-50
    - Only 3 Tp's in signal messages
    - 10% Tp1, 10% Tp2, 80% Tp3

'''
