import pandas as pd # type: ignore
from datetime import datetime
import os
import shutil
import numpy as np # type: ignore

from classes import Declaration
from templates import templates as temp

start_datetime = datetime.now()
start_datetime_str = start_datetime.strftime("%y%m%d%H%M%S")

archive = './archive/'
incomming_path = './incomming/'
outgoing_path = './outgoing/'

def main(file_path):
    global start_datetime, start_datetime_str

    start_datetime = datetime.now()
    start_datetime_str = start_datetime.strftime("%y%m%d%H%M%S")

    filename = os.path.basename(file_path)

    #function(filename)
    
    end_datetime = datetime.now()
    excecution_time = end_datetime - start_datetime
    print(f'Excecutiontime: {excecution_time}', flush=True)