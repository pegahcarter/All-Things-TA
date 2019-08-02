import numpy as np
from datetime import datetime, timedelta
import time
import ccxt

import numpy as np
import pandas as pd

def foo():
    data = [[1,1,1], [2,3,4], [10, 100, 1000]]
    # df = pd.DataFrame(data*i, columns=['col1', 'col2', 'col3'])
    return data

test1_a = []
for i in range(3):
    test1_a += foo()
test1_a

test1_b = [foo() for i in range(3)]
test1_b

# ------------------------------------------------------------------------------

def foo2():
    data = [[1,1,1], [2,3,4], [10, 100, 1000]]
    return pd.DataFrame(data, columns=['col1', 'col2', 'col3'])

test2_a = pd.DataFrame([])
for i in range(3):
    test2_a = test2_a.append(foo())
test2_a

test2_b = [foo2() for i in range(3)]
test2_b
len(test2_b)

test2_c = pd.DataFrame(columns=['col1', 'col2', 'col3'])
test2_c = test2_c.append([foo2() for i in range(3)], ignore_index=True)
test2_c


test2_d = pd.DataFrame(columns=['col1', 'col2', 'col3'])
test2_d = test2_d.append([foo() for i in range(3)], ignore_index=True)
test2_d

test3_a = pd.DataFrame([foo() for i in range(3)], columns=['col1', 'col2', 'col3'])
test3_a

test3_b = pd.DataFrame([])





# from py.variables import *
# from urllib.parse import urlencode
#
# url = 'https://api.telegram.org/bot' + API_KEY + '/sendMessage?'
# mydict = {'chat_id': CHAT_ID, 'text': 'Hello'}
# url + urlencode(mydict)
