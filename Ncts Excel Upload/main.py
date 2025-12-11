from tasks import NCTS_excel_upload
import time
import os

infinite_loop = os.environ.get('INFINITE_LOOP', 'False').lower() == 'true'

if __name__ == "__main__":
    while infinite_loop:
        try:
            print("Start Execution", flush=True)
            NCTS_excel_upload()
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
