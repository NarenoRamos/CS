from tasks import main
import time
import os

infinite_loop = os.environ.get('INFINITE_LOOP', 'False').lower() == 'true'

if __name__ == "__main__":
    while infinite_loop:
        try:
            print("Start Execution", flush=True)
            main()
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
