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

def main():
    incomming_directory = os.fsencode(incomming_path)

    for file in os.listdir(incomming_directory):
        # create file in outgoing dir
        return 0
    
    end_datetime = datetime.now()
    excecution_time = end_datetime - start_datetime
    print(f'Excecutiontime: {excecution_time}', flush=True)