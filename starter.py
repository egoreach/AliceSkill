import multiprocessing
import subprocess

import subscribing


if __name__ == "__main__":
    tg_process = multiprocessing.Process(target=subprocess.call, args=(['python', 'telegram.py'],))
    subscribing_process = multiprocessing.Process(target=subscribing.main)

    tg_process.start()
    subscribing_process.start()