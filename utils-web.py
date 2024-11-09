import os
import datetime
import requests
import json
import csv

import bs4
from user_agent import generate_user_agent

import os
import urllib.request, sys
from threading import Thread
import requests
import time

import utils


# --- Web scrapping methods ---

def generate_headers_with_user_agent(device_type='desktop', os=('mac', 'linux')):
     """
     Return examples:
     {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:46.0) Gecko/20100101 Firefox/46.0'}
     {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
     {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
     """
     return {'User-Agent': generate_user_agent(device_type=device_type, os=os)}


def get_page(url, headers, timeout=60):
        headers = headers or generate_headers_with_user_agent()
        return requests.get(url, headers=headers, timeout=timeout)


def save_page_resp(page_str, path):
    """
    Params:
    page_str (str): html page, 'requests' lib example: page_resp.text
    """
    if not page_str:
        return
    with open(path, 'w') as f:
        f.write(page_str)


def soup_page_example(page_str):
    """
    Example get values from html page using bs4

    Params:
    page_str (str): html page, 'requests' lib example: page_resp.text
    """
    soup = bs4.BeautifulSoup(page_str.text, features="html.parser")
    res = soup.find('div', attrs={'class': 'pagingResults'}).select('p')[0]
    foo = soup.find_all('div', attrs={'class': 'premiseBox'})
    for bar in foo:
            res = bar.select('h3 > a')[0]
    return res



# --- Misc stuff ---

class VideosDownloader:
    """
    Download videos (urls in .txt) in parallel
    Display downloading progress
    """
    CHUCK_SIZE=8192
    
    def __init__(self, to_download_file):
        self.to_download_file = to_download_file
        
        self._progresses = {}
        

    def start_videos_downloading(self):
        prefix = "peripheral_1"
        threads = []
        with open(self.to_download_file, 'r') as f:
            for i, url in enumerate(f):
                output = f"{prefix}_{i+1}.mp4"
                if url.endswith('\n'):
                    url = url[:-1]
                downloadThread = Thread(target=self.download_video, args=[url, output])
                downloadThread.start()
                threads.append(downloadThread)
        progressThread = Thread(target=self.updOutput)
        progressThread.start()
        progressThread.join()
        for t in threads:
            t.join()

    def download_video(self, url, output, chunk_size=CHUCK_SIZE):
        """
        Download a single video

        Params:
        chunk_size (int): size of the chunk to iterate over (in bytes)
        """
        
        resp = requests.get(url, stream=True)
        with open(output, 'wb') as f:
            # iterate over every chunk and calculate % of total
            for i, chunk in enumerate(resp.iter_content(chunk_size=chunk_size)):
                f.write(chunk)
                
                total_size = int(resp.headers['Content-Length']) # total size in bytes
                progress = ((i * chunk_size) / total_size) * 100 # calculate progress in percentage
                self._progresses[output] = round(progress, 2)
        self._progresses.pop(output)

    def _updProgressOutput(self):
        while True:
            progressOutput = ""
            for k, v in self._progresses.items():
                progressOutput += f"\r{k} {v}%...\r\n"
            print(progressOutput)
            time.sleep(1)
            utils.cls()
            if not self._progresses:
                break
