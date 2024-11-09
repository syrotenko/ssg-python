import os
import datetime
import requests
import json
import csv

import bs4
from user_agent import generate_user_agent

import logging
logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('example-logging')


# --- Misc stuff ---

def get_datetime_str(format_="%y%m%d_%H%M%S"):
    """ Return example: 241109_152703 """
    return datetime.datetime.now().strftime(format_)


def serialize_to_json_file(obj, path):
    """ Write python object to the json file. Create necessary dirs """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(obj, f)
        print()


def deserialize(path, obj_class):
    """ Read json file to python obj """
    with open(path, 'r') as f:
        data_raw = json.load(f)
        return obj_class(**data_raw)


def csv_write_example(iter_of_iters, path, dialect='excel', delimiter=';', is_rewrite_file=False):
     mode = 'w' if is_rewrite_file else 'a'
     with open(path, mode) as f:
            csv_writer = csv.writer(f, dialect=dialect, delimiter=delimiter)
            for row in iter_of_iters:
                csv_writer.writerow(row)


def csv_read_example(path, field_names, dialect='excel', delimiter=';'):
     with open(path, 'r') as f:
            reader = csv.DictReader(f, field_names, dialect=dialect, delimiter=delimiter)
            for row in reader:
                row['field_name'] = 'cell_value'



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
