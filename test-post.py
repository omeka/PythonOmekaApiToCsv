#!/usr/bin/env python
# -*- coding: utf-8 -*-

from omekaclient import OmekaClient
import yaml
import json

endpoint = "http://localhost/omeka/api"
apikey = "XXXXXXXXX"

# Here is an example of the kind of YAML user could create
# Filler text courtesy of http://hipsteripsum.me
ymlinput = """
---
Title: Another hipster item
Source: |
    <a href="http://hipsteripsum.me">Hipster Ipsum</a>
Publisher: Quinoa McDaniel
Date: ca. 2013
Rights: Open
Format: Plain text, of course
Language: Hipsterese
Type: Text
Description: |
    Yr cardigan viral, flannel food truck brunch mumblecore whatever. Selvage you
    probably haven't heard of them quinoa, meh mumblecore literally 90's 
    banh mi. Brunch flannel mixtape wayfarers meggings art party. Ethical ugh
    scenester viral 90's. Cornhole quinoa small batch, pop-up lomo mixtape 
    rights next level leggings Brooklyn stumptown cray VHS fanny pack. Neutra
    Carles +1 Cosby sweater, tousled banjo kale chips freegan single-origin 
    American Apparel pork belly Pinterest Banksy mlkshk synth. Pinterest
    fingerstache sustainable, ethical actually keytar next level ethnic hoodie
    post-ironic Shoreditch farm-to-table Thundercats.
Text: |
    <p>Single-origin <em>coffee</em> drinking vinegar Bushwick, Echo Park 90's
    Helvetica McSweeney's. Church-key American Apparel selvage sustainable.
    Sustainable mixtape cornhole direct trade church-key Wes Anderson. 8-bit
    salvia gentrify small batch shabby chic, single-origin coffee occupy
    messenger bag Helvetica ennui forage wayfarers. Jean shorts 8-bit bitters,
    sustainable retro VHS kogi Tumblr actually photo booth twee Terry
    Richardson squid cred fap. Polaroid Shoreditch keytar, Blue Bottle
    skateboard bitters twee letterpress VHS pour-over Schlitz master cleanse
    food truck. Wolf pug freegan Tumblr pork belly locavore, Carles distillery
    <strong>stumptown</strong> PBR 8-bit.</p>

    <p>Irony pug Portland occupy, next level fap tousled. Post-ironic raw denim
    organic leggings, deep v paleo Shoreditch twee selvage photo booth scenester
    90's wayfarers keffiyeh readymade. Keffiyeh McSweeney's keytar butcher 
    beard. Cray aesthetic PBR, tattooed photo booth chambray fanny pack banh mi.
    Craft beer Terry Richardson lo-fi, Echo Park master cleanse twee roof party
    Blue Bottle put a bird on it vinyl tofu mixtape fap fixie. Ennui 
    coffee gluten-free, Williamsburg Brooklyn master cleanse locavore Vice swag
    slow-carb disrupt lo-fi. Twee ethnic synth biodiesel.</p>
"""

# A dictionary of all the element ids in the Omeka database
# TODO: Figure out how to generate this dict using Omeka API elements resource
elements = {1:"Text",2:"Interviewer",3:"Interviewee",4:"Location",5:"Transcription",6:"Local URL",7:"Original Format",10:"Physical Dimensions",11:"Duration",12:"Compression",13:"Producer",14:"Director",15:"Bit Rate/Frequency",16:"Time Summary",17:"Email Body",18:"Subject Line",19:"From",20:"To",21:"CC",22:"BCC",23:"Number of Attachments",24:"Standards",25:"Objectives",26:"Materials",27:"Lesson Plan Text",28:"URL",29:"Event Type",30:"Participants",31:"Birth Date",32:"Birthplace",33:"Death Date",34:"Occupation",35:"Biographical Text",36:"Bibliography",37:"Contributor",38:"Coverage",39:"Creator",40:"Date",41:"Description",42:"Format",43:"Identifier",44:"Language",45:"Publisher",46:"Relation",47:"Rights",48:"Source",49:"Subject",50:"Title",51:"Type",58:"Additional Creator",59:"Transcriber",60:"Producer",61:"Render Device",62:"Render Details",63:"Capture Date",64:"Capture Device",65:"Capture Details",66:"Change History",67:"Watermark",69:"Encryption",70:"Compression",71:"Post Processing",72:"Width",73:"Height",74:"Bit Depth",75:"Channels",76:"Exif String",77:"Exif Array",78:"IPTC String",79:"IPTC Array",80:"Bitrate",81:"Duration",82:"Sample Rate",83:"Codec",84:"Width",85:"Height"}

# Reversing the keys and values of elements dictionary for easier lookup
d = {}
for key, val in elements.items():
   d[val] = key

# Settings that will apply to the item as a whole
# TODO: Make these optional user arguments for the script 
jsonobj = {"collection": {"id": 1}, "item_type":{"id":1}, "featured": False,"public": True}

# This is where the input YAML is converted into json and added to jsonobj
data = yaml.load(ymlinput)
element_texts = []
for key in data:
    element_text = {"html": True, "text": "none", "element_set": {"id": 0}}
    element = {}
    element["id"] = d[key]
    element_text["element"] = element
    element_text["text"] = data[key]
    element_texts.append(element_text)
jsonobj["element_texts"] = element_texts

# Dump json object into a string and post
jsonstr = json.dumps(jsonobj)
OmekaClient(endpoint, apikey).post("items", jsonstr) 
