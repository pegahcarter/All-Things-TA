import pandas as pd
from datetime import datetime

df = pd.read_csv('prices/BTC.csv')
df = df.dropna().reset_index(drop=True)

test = df[-1:].values[0]
# Remove milliseconds from date
test[0] = test[0][:-4]

last_date = datetime.strptime(test[0], '%Y-%m-%d %H:%M:%S')

'BTC - ' + test[-1]
last_date = last_date.strftime('%H:%M %p %B %d ')
