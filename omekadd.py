#!/usr/bin/env python
# -*- coding: utf-8 -*-

endpoint = "http://localhost/omeka/api"
apikey = "XXXXXXXXXXXXX"

from omekaclient import OmekaClient
from sys import stdin
import argparse
import yaml
import json
try:
    import markdown
except ImportError:
    print "Error: Python module for Markdown missing"

# Define and parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('inputfile', type=file, nargs="?", default=stdin, help='Name of input YAML file (optional)')
parser.add_argument('-p', '--public', action='store_true', help='Make item public')
parser.add_argument('-f', '--featured', action='store_true', help='Make item featured')
parser.add_argument('-c', '--collection', type=int, default=None, help='Add item to collection n')
parser.add_argument('-t', '--type', type=int, default=1, help='Specify item type using Omeka id; default is 1, for "Document"')
parser.add_argument('-u', '--upload', default=None, help='Name of file to upload and attach to item')
parser.add_argument('-m', '--mdmark', default="markdown>", help='Change string prefix that triggers markdown conversion; default is "markdown>"')
args = vars(parser.parse_args())

# A dictionary of all the element ids in the Omeka database
# TODO: Figure out how to generate this dict using Omeka API elements resource
elements = {1:"Text",2:"Interviewer",3:"Interviewee",4:"Location",5:"Transcription",6:"Local URL",7:"Original Format",10:"Physical Dimensions",11:"Duration",12:"Compression",13:"Producer",14:"Director",15:"Bit Rate/Frequency",16:"Time Summary",17:"Email Body",18:"Subject Line",19:"From",20:"To",21:"CC",22:"BCC",23:"Number of Attachments",24:"Standards",25:"Objectives",26:"Materials",27:"Lesson Plan Text",28:"URL",29:"Event Type",30:"Participants",31:"Birth Date",32:"Birthplace",33:"Death Date",34:"Occupation",35:"Biographical Text",36:"Bibliography",37:"Contributor",38:"Coverage",39:"Creator",40:"Date",41:"Description",42:"Format",43:"Identifier",44:"Language",45:"Publisher",46:"Relation",47:"Rights",48:"Source",49:"Subject",50:"Title",51:"Type",58:"Additional Creator",59:"Transcriber",60:"Producer",61:"Render Device",62:"Render Details",63:"Capture Date",64:"Capture Device",65:"Capture Details",66:"Change History",67:"Watermark",69:"Encryption",70:"Compression",71:"Post Processing",72:"Width",73:"Height",74:"Bit Depth",75:"Channels",76:"Exif String",77:"Exif Array",78:"IPTC String",79:"IPTC Array",80:"Bitrate",81:"Duration",82:"Sample Rate",83:"Codec",84:"Width",85:"Height"}

# Reversing the keys and values of elements dictionary for easier lookup
d = {}
for key, val in elements.items():
   d[val] = key

# Get YAML from input file
yamlinput = args['inputfile'].read()

# Set general item settings using command line arguments or defaults
# Defaults are to make items private, not featured, no collection documents
jsonobj = {"collection": {"id": args["collection"]}, "item_type": {"id": args["type"]}, "featured": args["featured"], "public": args["public"]}

# This is where the input YAML is converted into json and added to jsonobj
data = yaml.load(yamlinput)
element_texts = []
for key in data:
    element_text = {"html": True, "text": "none", "element_set": {"id": 0}}
    element = {"id": d[key]}
    element_text["element"] = element
    text = str(data[key])
    if text.startswith(args["mdmark"]):
       element_text["text"] = markdown.markdown(text[len(args["mdmark"]):])
    else:
       element_text["text"] = text
    element_texts.append(element_text)
jsonobj["element_texts"] = element_texts

# Dump json object into a string and post, printing API response
jsonstr = json.dumps(jsonobj)
response, content = OmekaClient(endpoint, apikey).post("items", jsonstr) 
location = response["location"]
print response.reason, location

# Optionally, upload and attach file to new item
if args["upload"] is not None:
    print "Uploading file ..."
    uploadjson = {"item": {"id": int(location.split("/")[-1])}}
    uploadmeta = json.dumps(uploadjson)
    uploadfile = open(args["upload"], "r").read()
    response, content = OmekaClient(endpoint, apikey).post_file(uploadmeta, args["upload"], uploadfile) 
    print response.reason, response["location"]
