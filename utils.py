import os
import datetime
import json
import csv

import logging
logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('example-logging')


# --- Misc stuff ---

def cls():
    os.system('clear')


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
