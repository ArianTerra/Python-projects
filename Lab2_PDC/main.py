import os
import datetime
# pip packages
import wget

def main():
    URL = "https://raw.githubusercontent.com/ArianTerra/Python-projects/master/Lab2_PDC/nagatoro.jpg"
    download_file(URL)


"""
Downloads a file to 'Downloads/' dir.
Adds a timestamp to the file name to ensure that different file copies are stored.
"""
def download_file(url : str):
    time_now = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    base_file_name = os.path.basename(url)
    file_name, file_ext = os.path.splitext(base_file_name)
    new_name = file_name + '_' + time_now + '.' + file_ext
    wget.download(url, "Downloads/" + new_name)

if __name__ == '__main__':
    main()
