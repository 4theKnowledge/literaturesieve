"""
Multiprocessing for parallel text processing.
@src: https://www.youtube.com/watch?v=fKl2JW_qrso
@author: Tyler Bikaun
"""
import concurrent.futures

import time

def do_something(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return f'Done sleeping...{seconds}'


def main():

    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:   # can change from Process to Thread; Thread - IO bound (open/save); Process - CPU bound
        secs = [5,4,3,2,1]    # iterables
        results = executor.map(do_something, secs)   # returns result (order of start) not futures (order of finish)

        for result in results:
            # handle exceptions here; they're not raised when running.
            print(result)

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} seconds(s)')

if __name__ == '__main__':
    main()