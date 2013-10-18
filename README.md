omekadd
=======

A script for adding new items to Omeka from the command line using simple YAML
documents, using the Omeka API and Python

Caleb McDaniel, <http://wcm1.web.rice.edu>

Description
-----------

The [Omeka
API](https://omeka.readthedocs.org/en/latest/Reference/api/index.html)
(available in Omeka 2.1) makes it possible to add new items to a
database from the commandline, but to make the API request you have to
represent the item in JSON. That is, to add a new item, you would have
to construct a string that looks something like this:

~~~~ {.json}
{"element_texts": [{"text": "Quinoa McDaniel", "element_set": {"id": 0}, "html": true, "element": {"id": 45}}, {"text": "<p>This item was added to this site using the <a href=\"https://omeka.readthedocs.org/en/latest/Reference/api/index.html\">Omeka API</a>\nand a script called <a href=\"https://github.com/wcaleb/omekadd\"><code>omekadd</code></a>,\nwhich transforms YAML documents into JSON strings suitable for using\nwith the API. As this Description demonstrates, the script can also\nconvert <a href=\"http://daringfireball.net/projects/markdown/\">Markdown</a> into\nHTML for easy formatting. The other text in this item was taken from\nHipster Ipsum, a random generator of Hipsterese.</p>", "element_set": {"id": 0}, "html": true, "element": {"id": 41}}, {"text": "Hipsterese", "element_set": {"id": 0}, "html": true, "element": {"id": 44}}, {"text": "Open", "element_set": {"id": 0}, "html": true, "element": {"id": 47}}, {"text": "<p>Single-origin <em>coffee</em> drinking vinegar Bushwick, Echo Park 90's\nHelvetica McSweeney's. Church-key American Apparel selvage sustainable.\nSustainable mixtape cornhole direct trade church-key Wes Anderson. 8-bit\nsalvia gentrify small batch shabby chic, single-origin coffee occupy\nmessenger bag Helvetica ennui forage wayfarers. Jean shorts 8-bit bitters,\nsustainable retro VHS kogi Tumblr actually photo booth twee Terry\nRichardson squid cred fap. Polaroid Shoreditch keytar, Blue Bottle\nskateboard bitters twee letterpress VHS pour-over Schlitz master cleanse\nfood truck. Wolf pug freegan Tumblr pork belly locavore, Carles distillery\n<strong>stumptown</strong> PBR 8-bit.</p>", "element_set": {"id": 0}, "html": true, "element": {"id": 1}}, {"text": "Plain text, of course", "element_set": {"id": 0}, "html": true, "element": {"id": 42}}, {"text": "ca. 2013", "element_set": {"id": 0}, "html": true, "element": {"id": 40}}, {"text": "<a href=\"http://hipsteripsum.me\">Hipster Ipsum</a>\n", "element_set": {"id": 0}, "html": true, "element": {"id": 48}}, {"text": "Sample item added with omekadd", "element_set": {"id": 0}, "html": true, "element": {"id": 50}}, {"text": "Text", "element_set": {"id": 0}, "html": true, "element": {"id": 51}}], "item_type": {"id": 1}, "featured": false, "public": false, "collection": {"id": null}}
~~~~

This script makes adding items easier by allowing you to instead
represent the new item with a well-formed YAML file, which looks more
like this:

    ---
    Title: Sample item added with omekadd
    Source: Hipster Ipsum
    Publisher: Quinoa McDaniel
    Date: ca. 2013
    Rights: Open
    Format: Plain text, of course
    Language: Hipsterese
    Type: Text
    Description: |
        markdown> This item was added to this site using the Omeka API
        and a script called [`omekadd`](https://github.com/wcaleb/omekadd),
        which transforms YAML documents into JSON strings suitable for using
        with the API. As this Description demonstrates, the script can also
        convert [Markdown](http://daringfireball.net/projects/markdown/) into
        HTML for easy formatting. The other text in this item was taken from
        Hipster Ipsum, a random generator of Hipsterese.
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

The script turns the YAML document into the JSON string and posts it to
your Omeka database using the API endpoint specified at the top of the
script.

Installation
------------

Make sure you have downloaded and installed Omeka 2.1 so you can use the API features.

Clone this repo:

	git clone https://github.com/wcaleb/omekadd.git

The `omekadd.py` script imports the `OmekaClient` class from `omekaclient.py`,
which is included in the repo. The development repo for the Omeka Client is
maintained by [Jim Safley](https://github.com/jimsafley/omeka-client-py), who
wrote the original client.

Edit the first two lines of `omekadd.py` so that they contain your API
endpoint and your API key. See the [Omeka
documentation](https://omeka.readthedocs.org/en/latest/Reference/api/for_beginners.html)
for help.

To test, make sure that you've changed the permissions on `omekadd.py` to make
it executable, and then try posting the `sample.yml` to your database:

	cd omekadd
	./omekadd.py sample.yaml

Read on to discover more features, like uploading files to attach to the item!

Usage
-----

In a text editor, type up your new item as a [YAML
document](http://en.wikipedia.org/wiki/YAML). **The YAML document must
be well-formed.** You can validate your YAML
[here](http://yamllint.com).

The keys in your YAML (the words to the left of the colons) should
correspond to the item element texts in the Omeka database. These are the
things that you typically see when you fill out the webform in Omeka,
like the names of the Dublin Core fields or the Item Type Metadata
fields.

Next, run the script, supplying the name of your input YAML file
immediately after the script name.

For example, [this item](http://wcaleb.rice.edu/omeka/items/show/94) in
my Omeka database was added using the `sample.yaml` file in this
repository and this command:

    ./omekadd.py sample.yaml

Alternatively, you can pipe your YAML to the script as `stdin` instead.

**Note:** The script will treat every field as though you had clicked
"Use HTML" when filling out the webform. That means that so long as you
properly escape the HTML, you can include HTML in your YAML file. The
easiest way to do this is to use YAML's [literal
blocks](http://en.wikipedia.org/wiki/YAML#Block_literals), as shown in
the sample file.

Options
-------

By default, `omekadd` creates an item that is a private, non-featured
Document without a collection. But you can change these defaults using
the command-line arguments:

      -h, --help            show this help message and exit
      -p, --public          Make item public
      -f, --featured        Make item featured
      -c COLLECTION, --collection COLLECTION
                            Add item to collection COLLECTION
      -t TYPE, --type TYPE  Specify item type using Omeka id; default is 1, for
                            "Document"

Markdown Functionality
----------------------

If you have the Python markdown module, you can also use Markdown in
your YAML. To do this, first install the module:

    pip install markdown

Then, in your YAML file, prefix any string that you would like to be converted
from Markdown to HTML with a special prefix. By default, as shown in the
`sample.yaml` file, this is set to the string `markdown>`. However, you can
change the prefix mark on the commandline by using the `--mdmark` option.

*Note:* If you process a string with Markdown, the output HTML will be wrapped
in `<p>` and `</p>` tags. That's a feature of Markdown, but it may clutter your
item metadata with unwanted tags.

File Uploading
--------------

You can also upload a file to attach to your new item using this script.
Just use the argument `-u, --upload` at the command line, followed by the
properly escaped name of the file you want to upload. After creating your new
Omeka item, the script will get the new item's ID and then upload the new file,
associating it with the new item.

Issues
------

Right now this is just a barebones proof-of-concept script, so I'm certain
there are bugs to be worked out. Please help test it and don't be shy about
reporting issues or forking and improving it. I've mainly made the script to
help in my workflow, so I'm sure there are more pythonic ways to do this, and
I'd be grateful for tips.
