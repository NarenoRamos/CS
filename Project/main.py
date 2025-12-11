from tasks import #fucntion in taskfolder
import time
import os

infinite_loop = os.environ.get('INFINITE_LOOP', 'False').lower() == 'true'

if __name__ == "__main__":
    while infinite_loop:
        try:
            print("Start Execution", flush=True)
            #fucntion 
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
