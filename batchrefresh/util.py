import json
from collections import namedtuple
import os
import shutil

def _json_object_hook(d): 
    return namedtuple('X', d.keys())(*d.values())
def json2obj(data): 
    return json.loads(data, object_hook=_json_object_hook)

def xcopy(src,dest):
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, dest)