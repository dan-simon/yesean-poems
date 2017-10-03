import os
import re

entry_pattern = r'\d+\.html'

def sort_files(l):
    return list(sorted(l, key=lambda x: int(x.split('.')[0])))

def get_posts():
    return sort_files(i for i in os.listdir('.') if re.match(entry_pattern, i))