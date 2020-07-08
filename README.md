Omeka API to CSV Script
=======================

This repo includes a Python script which allows users to generate CSV files of the metadata in their Omeka installations. It will retreive the metadata for items, collections, element sets, elements, files, tags, exhibits, and exhibit pages. However, it does not retreive the files themselves. Only the metadata associated with them.

Instructions
============

Download the ZIP of the the script from above, or from [here](https://github.com/omeka/PythonOmekaApiToCsv/archive/master.zip)

(Alternatively, you can clone this repository.)

Unzip the package somewhere on your local computer.

Open a command-line interface, and navigate to the newly created directory (/PythonOmekaApiToCsv).

Execute the script by entering the following command:
    
    python omekacsv.py

You will now be prompted to enter your Omeka API [endpoint](http://omeka.readthedocs.org/en/latest/Reference/api/for_beginners.html#omeka-s-rest-api)

At this point, you are prompted to enter an Omeka API key. If you are using an API key to export non-public material, enter it now. If all of your materials are public, or you only want materials that are public, you may skip this step.

You will also be prompted to choose a character to use as a separator when multiple values appear in a single cell (for example, when there is more than one text entered for the same element for an item). This character should be one that doesn't appear anywhere in the actual data being exported. By default, the script will use the | ("pipe") character.

The script will now generate a series of CSV files for each of your resource types within the current directory.

Attribution
===========

This script is based on omekacsv.py, originally developed by Caleb McDaniel, <http://wcm1.web.rice.edu>. Original code can be found at https://github.com/wcaleb/omekadd
