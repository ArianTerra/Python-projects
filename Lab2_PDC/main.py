import os
import datetime
import glob
import time
import shutil
import csv
import threading
from threading import Thread
# pip packages in requirements.txt
import wget
from colorama import Fore

# folders
DOWNLOADS = "Downloads/"
TEMP = "Temp/"

# config
URL = "https://raw.githubusercontent.com/ArianTerra/Python-projects/master/Lab2_PDC/nagatoro.jpg"
COUNT = 2 # how much time download a file

def main():
    print(Fore.BLUE + "COMPARING DOWNLOAD METHODS" + Fore.RESET)
    # download comparing
    print(Fore.YELLOW + "Download one by one" + Fore.RESET)
    download_mono = test_download_mono()
    print(Fore.YELLOW + "Download multithreaded" + Fore.RESET)
    download_thread = test_download_thread()
    
    # copy comparing
    print(Fore.BLUE + "COMPARING COPY METHODS" + Fore.RESET)
    print(Fore.YELLOW + "Copy one by one" + Fore.RESET)
    copy_mono = test_copy_mono()
    print(Fore.YELLOW + "Copy multithreaded" + Fore.RESET)
    copy_thread = test_copy_thread()
    
    # csv files reader
    print(Fore.BLUE + "WRITING CSV FILES" + Fore.RESET)
    f_d = open("Results/Download.csv", "w")
    f_c = open("Results/Copy.csv", "w")
    writer_d = csv.writer(f_d)
    writer_c = csv.writer(f_c)
    header = ["Files&Threads", "Mono", "Threaded"]
    writer_d.writerow(header)
    writer_c.writerow(header)
    
    for i in range(COUNT):
        writer_d.writerow([i+1, download_mono[i], download_thread[i]])
        writer_c.writerow([i+1, copy_mono[i], copy_thread[i]])
    f_d.close()
    f_c.close()
    print("Download method results written to Results/Download.csv\nCopy method results written to Results/Copy.csv")
    
    print(Fore.GREEN + "Measuring completed. Results written to Results/ folder" + Fore.RESET)
            
def test_download_mono():
    time_result = []
    for i in range(1, COUNT+1):
        time_start = time.time()
        for j in range(i):
            download_file(URL)
        time_end = time.time()
        elapsed = "{:.6f}".format(time_end - time_start)
        print(f"Downloaded {i} files. Time: {elapsed} s")
        time_result.append(elapsed)
    clear_folder(DOWNLOADS)
    return time_result

def test_copy_mono():
    time_result = []
    for i in range(1, COUNT+1):
        for j in range(i):
            download_file(URL)
        files = glob.glob(DOWNLOADS + '*')
        time_start = time.time()
        for file in files:
            copy_to_temp(file)
        time_end = time.time()
        elapsed = "{:.6f}".format(time_end - time_start)
        print(f"Copied {i} files. Time: {elapsed} s")
        time_result.append(elapsed)
        clear_folder(DOWNLOADS)
        clear_folder(TEMP)
    return time_result
    
def test_download_thread():
    time_result = []
    for i in range(1, COUNT+1):
        threads = []
        for j in range(i):
            th = Thread(target=download_file, args=(URL, ))
            threads.append(th)
        # start all threads
        time_start = time.time()
        for x in threads:
            x.start()
        # wait for all to finish using .join()
        for x in threads:
            x.join()
        time_end = time.time()
        elapsed = "{:.6f}".format(time_end - time_start)
        print(f"Downloaded {i} files. Time: {elapsed} s")
        time_result.append(elapsed)
    clear_folder(DOWNLOADS)
    return time_result
    
def test_copy_thread():
    time_result = []
    for i in range(1, COUNT+1):
        threads = []
        for j in range(i):
            file = download_file(URL)
            th = Thread(target=copy_to_temp, args=(file, ))
            threads.append(th)
            
        
        # start all threads
        time_start = time.time()
        for x in threads:
            x.start()
        # wait for all to finish using .join()
        for x in threads:
            x.join()
        time_end = time.time()
        elapsed = "{:.6f}".format(time_end - time_start)
        print(f"Copied {i} files. Time: {elapsed} s")
        time_result.append(elapsed)
        clear_folder(DOWNLOADS)
        clear_folder(TEMP)
    return time_result

"""
Downloads a file to 'Downloads/' dir.
Adds a timestamp to the file name to ensure that different file copies are stored.
"""
def download_file(url : str):
    time_now = datetime.datetime.now().strftime("%y%m%d_%H%M%S_%f")
    base_file_name = os.path.basename(url)
    file_name, file_ext = os.path.splitext(base_file_name)
    new_name = file_name + '_' + time_now + file_ext
    downloaded = wget.download(url, DOWNLOADS + new_name)
    print() # new line after wget
    return downloaded

def copy_to_temp(file):
    file_name = os.path.basename(file)
    shutil.copy(file, TEMP + file_name)

"""
Removes all files from a folder.
"""
def clear_folder(path : str):
    files = glob.glob(path + '*')
    for f in files:
        os.remove(f)
    print(path + " folder cleared")
    

if __name__ == '__main__':
    main()
