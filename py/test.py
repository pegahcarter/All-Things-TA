from py.variables import *
from urllib import quote_plus
import requests

message = 'https://api.telegram.org/bot' + API_KEY
message += '/sendMessage?chat_id=' + CHAT_ID
message += '&text=' + quote_plus('Hello')
requests.get(message)
