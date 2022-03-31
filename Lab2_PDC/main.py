import os
import datetime
import glob
import time
# pip packages in requirements.txt
import wget
import shutils

# folders
DOWNLOADS = "Downloads/"
TEMP = "Temp/"

# config
URL = "https://raw.githubusercontent.com/ArianTerra/Python-projects/master/Lab2_PDC/nagatoro.jpg"
COUNT = 3 # how much time download a file

def main():
    # file download time measurment
    for i in range(1, COUNT+1):
        time_start = time.time()
        for j in range(i):
            download_file(URL)
        time_end = time.time()
        elapsed = "{:.4f}".format(time_end - time_start)
        print(f"Downloaded {i} files. Time: {elapsed} s")
    clear_folder(DOWNLOADS)
    
    # file copy time measurment

"""
Downloads a file to 'Downloads/' dir.
Adds a timestamp to the file name to ensure that different file copies are stored.
"""
def download_file(url : str):
    time_now = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    base_file_name = os.path.basename(url)
    file_name, file_ext = os.path.splitext(base_file_name)
    new_name = file_name + '_' + time_now + '.' + file_ext
    downloaded = wget.download(url, DOWNLOADS + new_name)
    print() # new line after wget
    return downloaded

"""
Removes all files from a folder.
"""
def clear_folder(path : str):
    files = glob.glob(path + '*')
    for f in files:
        os.remove(f)

if __name__ == '__main__':
    main()
