# Contains the helper functions
import os
import yaml
import requests
import time
import ccxt

from datetime import datetime, timedelta
from urllib.parse import urlencode

import pandas as pd
import numpy as np


with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.Loader)



def determine_csv_filename(channel):
    return f"{os.path.abspath('../')}/data/signals/{channel}.csv"
