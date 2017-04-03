"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import mappings

osmfile = "cleveland_ohio.xml"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]


def audit_street_type(street_types, street_name):
    # Check to make sure there are no unexpected characters in the street name
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected: 
            # Add the non-standard street names to a set within a dictionary
            street_types[street_type].add(street_name)

# Check if the tag refers to a street name
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "rb")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag): #Check to see if the tag contains a street name
                    audit_street_type(street_types, tag.attrib['v']) # Find the problematic street names
    osm_file.close()
    return street_types

street_mapping = mappings.street_mapping

def clean(name):
    name = name.split(" ")
    if name[-1] in street_mapping:
        name[-1] = street_mapping[name[-1]]
    name = ' '.join(name)
    return name

count_dict = {}

'''
if __name__ == '__main__':
    street_types = audit(osmfile)
    for street in street_types:
        count_dict[street] = len(street_types[street])
'''
for street in mappings.street_mapping:
    print("{} --> {}".format(street, street_mapping[street]))