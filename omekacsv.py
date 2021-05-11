#! /usr/bin/python

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict
import csv
import json
import math
import time
try:
    import readline
except ImportError:
    pass

try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.error import URLError, HTTPError
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, URLError, HTTPError

'''
Extract top-level metadata and element_texts from items returned by
Omeka 2.x API request, and then write to a CSV file. Intended for
requests to items, collections, element sets, elements, files, tags, exhibits, and exhibit pages.

Based on Caleb McDaniel's original Python CSV file generator: https://github.com/wcaleb/omekadd
'''

try:
    input = raw_input
except NameError:
    pass

try:
    unicode
    py2 = True
except NameError:
    unicode = str
    py2 = False

def request(endpoint, resource, query={}):
    url = endpoint + "/" + resource
    if apikey is not None:
        query["key"] = apikey
    url += "?" + urlencode(query)

    response = urlopen(url)
    return response.info(), response.read()

def unicodify(v):
    if type(v) is list or type(v) is dict:
        return None
    if type(v) is bool or type(v) is int or type(v) is float:
       return unicode(v)
    return v

def get_all_pages(endpoint, resource, pages):
    data = []
    page = 1
    while page <= pages:
        print('Getting results page ' + str(page) + ' of ' + str(pages) + ' ...')
        response, content = request(endpoint, resource, {'page': str(page), 'per_page': '50'})
        data.extend(json.loads(content))
        page += 1
        time.sleep(1)
    return data

endpoint = ''
while not endpoint:
    endpoint = input('Enter your Omeka API endpoint\n')
apikey = input('\nIf you are using an API key, please enter it now. Otherwise press Enter.\n')
if not apikey:
    apikey = None
multivalue_separator = input('\nEnter a character to separate mutiple values within a single cell.\nThis character must not be used anywhere in your actual data.\nLeave blank to use the default separator: |\n')
if not multivalue_separator:
    multivalue_separator = '|'

# get list of supported resources by this site
response, content = request(endpoint, 'resources')
available_resources = json.loads(content)

resources = ['items', 'files', 'elements', 'element_sets', 'tags', 'exhibits', 'exhibit_pages', 'geolocations']
for resource in resources:
    if (resource not in available_resources):
        continue

    print('Exporting ' + resource)

    # make initial API request; get max pages
    response, content = request(endpoint, resource)
    pages = int(math.ceil(float(response['omeka-total-results'])/50))

    # get all pages
    data = get_all_pages(endpoint, resource, pages)

    fields = []
    csv_rows = []

    for D in data:
        csv_row = {}

        for k, v in D.items():
            if k == 'tags':
                tags = [ tag['name'] for tag in v ]
                csv_row['tags'] = ','.join(tags)
            elif k == 'element_texts':
                texts_by_element = defaultdict(list)
                for element_text in v:
                    element_header = element_text['element_set']['name'] + ':' + element_text['element']['name']
                    texts_by_element[element_header].append(element_text['text'])
                for element_header, texts in texts_by_element.items():
                    csv_row[element_header] = multivalue_separator.join(texts)
            elif k == 'page_blocks':
                text = [ block['text'] for block in v ]
                csv_row['Text'] = multivalue_separator.join(filter(None, text))
            elif type(v) is dict:
                for subkey, subvalue in v.items():
                    if (subkey == 'url' or subkey == 'resource'):
                        continue
                    subvalue_string = unicodify(subvalue)
                    if subvalue_string is not None:
                        csv_row[k + '_' + subkey] = subvalue_string
                continue;
            elif type(v) is list or v is None:
                continue;
            else:
                csv_row[k] = unicodify(v)

        for k in csv_row.keys():
            if k not in fields: fields.append(k)
        csv_rows.append(csv_row)

    fields = sorted(fields, key=lambda field: (field != 'id', field))
    if (py2):
        o = open(resource + '_output.csv', 'wb')
        c = csv.DictWriter(o, [f.encode('utf-8', 'replace') for f in fields], extrasaction='ignore')
        c.writeheader()
        for row in csv_rows:
            c.writerow({k:v.encode('utf-8', 'replace') for k,v in row.items() if isinstance(v, unicode)})
    else:
        o = open(resource + '_output.csv', 'w', encoding='utf-8', newline='')
        c = csv.DictWriter(o, fields, extrasaction='ignore')
        c.writeheader()
        for row in csv_rows:
            c.writerow(row)
    o.close()
    print('File created: ' + resource + '_output.csv')
