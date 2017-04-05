#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
After auditing is complete the next step is to prepare the data to be inserted into a SQL database.
To do so you will parse the elements in the OSM XML file, transforming them from document format to
tabular format, thus making it possible to write to .csv files.  These csv files can then easily be
imported to a SQL database as tables.

The process for this transformation is as follows:
- Use iterparse to iteratively step through each top level element in the XML
- Shape each element into several data structures using a custom function
- Utilize a schema and validation library to ensure the transformed data is in the correct format
- Write each data structure to the appropriate .csv files

We've already provided the code needed to load the data, perform iterative parsing and write the
output to csv files. Your task is to complete the shape_element function that will transform each
element into the correct format. To make this process easier we've already defined a schema (see
the schema.py file in the last code tab) for the .csv files and the eventual tables. Using the 
cerberus library we can validate the output against this schema to ensure it is correct.

## Shape Element Function
The function should take as input an iterparse Element object and return a dictionary.

### If the element top level tag is "node":
The dictionary returned should have the format {"node": .., "node_tags": ...}

The "node" field should hold a dictionary of the following top level node attributes:
- id
- user
- uid
- version
- lat
- lon
- timestamp
- changeset
All other attributes can be ignored

The "node_tags" field should hold a list of dictionaries, one per secondary tag. Secondary tags are
child tags of node which have the tag name/type: "tag". Each dictionary should have the following
fields from the secondary tag attributes:
- id: the top level node id attribute value
- key: the full tag "k" attribute value if no colon is present or the characters after the colon if one is.
- value: the tag "v" attribute value
- type: either the characters before the colon in the tag "k" value or "regular" if a colon
        is not present.

Additionally,

- if the tag "k" value contains problematic characters, the tag should be ignored
- if the tag "k" value contains a ":" the characters before the ":" should be set as the tag type
  and characters after the ":" should be set as the tag key
- if there are additional ":" in the "k" value they and they should be ignored and kept as part of
  the tag key. For example:

  <tag k="addr:street:name" v="Lincoln"/>
  should be turned into
  {'id': 12345, 'key': 'street:name', 'value': 'Lincoln', 'type': 'addr'}

- If a node has no secondary tags then the "node_tags" field should just contain an empty list.

The final return value for a "node" element should look something like:

{'node': {'id': 757860928,
          'user': 'uboot',
          'uid': 26299,
       'version': '2',
          'lat': 41.9747374,
          'lon': -87.6920102,
          'timestamp': '2010-07-22T16:16:51Z',
      'changeset': 5288876},
 'node_tags': [{'id': 757860928,
                'key': 'amenity',
                'value': 'fast_food',
                'type': 'regular'},
               {'id': 757860928,
                'key': 'cuisine',
                'value': 'sausage',
                'type': 'regular'},
               {'id': 757860928,
                'key': 'name',
                'value': "Shelly's Tasty Freeze",
                'type': 'regular'}]}

### If the element top level tag is "way":
The dictionary should have the format {"way": ..., "way_tags": ..., "way_nodes": ...}

The "way" field should hold a dictionary of the following top level way attributes:
- id
-  user
- uid
- version
- timestamp
- changeset

All other attributes can be ignored

The "way_tags" field should again hold a list of dictionaries, following the exact same rules as
for "node_tags".

Additionally, the dictionary should have a field "way_nodes". "way_nodes" should hold a list of
dictionaries, one for each nd child tag.  Each dictionary should have the fields:
- id: the top level element (way) id
- node_id: the ref attribute value of the nd tag
- position: the index starting at 0 of the nd tag i.e. what order the nd tag appears within
            the way element

The final return value for a "way" element should look something like:

{'way': {'id': 209809850,
         'user': 'chicago-buildings',
         'uid': 674454,
         'version': '1',
         'timestamp': '2013-03-13T15:58:04Z',
         'changeset': 15353317},
 'way_nodes': [{'id': 209809850, 'node_id': 2199822281, 'position': 0},
               {'id': 209809850, 'node_id': 2199822390, 'position': 1},
               {'id': 209809850, 'node_id': 2199822392, 'position': 2},
               {'id': 209809850, 'node_id': 2199822369, 'position': 3},
               {'id': 209809850, 'node_id': 2199822370, 'position': 4},
               {'id': 209809850, 'node_id': 2199822284, 'position': 5},
               {'id': 209809850, 'node_id': 2199822281, 'position': 6}],
 'way_tags': [{'id': 209809850,
               'key': 'housenumber',
               'type': 'addr',
               'value': '1412'},
              {'id': 209809850,
               'key': 'street',
               'type': 'addr',
               'value': 'West Lexington St.'},
              {'id': 209809850,
               'key': 'street:name',
               'type': 'addr',
               'value': 'Lexington'},
              {'id': '209809850',
               'key': 'street:prefix',
               'type': 'addr',
               'value': 'West'},
              {'id': 209809850,
               'key': 'street:type',
               'type': 'addr',
               'value': 'Street'},
              {'id': 209809850,
               'key': 'building',
               'type': 'regular',
               'value': 'yes'},
              {'id': 209809850,
               'key': 'levels',
               'type': 'building',
               'value': '1'},
              {'id': 209809850,
               'key': 'building_id',
               'type': 'chicago',
               'value': '366409'}]}
"""

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import cerberus
import schema
import audit_amenities
import audit_dates
import audit_elevation
import audit_street_types
import audit_zip

OSM_PATH = "cleveland_ohio.xml"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "node_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "way_nodes.csv"
WAY_TAGS_PATH = "way_tags.csv"
RELATIONS_PATH = "relations.csv"
RELATION_MEMBERS_PATH = "relation_members.csv"
RELATION_TAGS_PATH = "relation_tags.csv"

COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+', re.IGNORECASE)
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']
RELATION_FIELDS = ['id', 'user', 'uid', 'version', 'timestamp', 'changeset']
RELATION_MEMBERS_FIELDS = ['id', 'member_id', 'role', 'type', 'position']
RELATION_TAGS_FIELDS = ['id', 'key', 'value', 'type']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  relation_attr_fields = RELATION_FIELDS, problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    
    """Clean and shape node, way, or relation, XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    relation_attribs = {}
    relation_members = []
    way_nodes = []
    tags = []  # Handle secondary tags the same way for node, way, and relation elements

    # Handle the element if it is a node
    if element.tag == 'node':
        node_id = element.attrib['id']

        #Handle the information in the top level node element attributes
        for key, value in element.items():
            if key in NODE_FIELDS:
                node_attribs[key] = value

        # Iterate through all the "tag" tags under the node element
        for tag in element.iter('tag'):

            # Pass on any tags with a problem character in the k attribute
            if PROBLEMCHARS.search(tag.attrib['k']):
                continue
            else:
                secondary_tag_dict = {}
                secondary_tag_dict['id'] = node_id
                key = tag.attrib['k']
                secondary_tag_dict['key'] = key                
                
                # Cleaning the elevation data tags
                if key == 'ele':
                    elevation = tag.attrib['v']
                    elevation = audit_elevation.clean(elevation)
                    if not elevation:
                        continue # Remove the elevation dicts that are not valid
                    secondary_tag_dict['value'] = elevation
                    secondary_tag_dict['type'] = 'regular'

                # Cleaning the street data tags
                elif key == 'addr:street' or key =='name':
                    street = tag.attrib['v']
                    street = audit_street_types.clean(street)
                    secondary_tag_dict['value'] = street
                    secondary_tag_dict['type'] = 'regular'

                # Clean the zip code data tags
                elif 'zip_left' in key:
                    zip_code = tag.attrib['v']
                    zip_code = audit_zip.clean(zip_code)
                    if not zip_code:
                        continue # Remove the zip codes that are not valid
                    secondary_tag_dict['value'] = zip_code
                    secondary_tag_dict['key'] = 'zip_left'
                    secondary_tag_dict['type'] = 'tiger'

                elif 'zip_right' in key:
                    zip_code = tag.attrib['v']
                    zip_code = audit_zip.clean(zip_code)
                    if not zip_code:
                        continue # Remove the zip codes that are not valid
                    secondary_tag_dict['value'] = zip_code
                    secondary_tag_dict['key'] = 'zip_right'
                    secondary_tag_dict['type'] = 'tiger'

                elif 'postcode' in key:
                    zip_code = tag.attrib['v']
                    zip_code = audit_zip.clean(zip_code)
                    if not zip_code:
                        continue # Remove the zip codes that are not valid
                    secondary_tag_dict['value'] = zip_code
                    secondary_tag_dict['key'] = 'postcode'
                    secondary_tag_dict['type'] = 'addr'

                # Clean the dates in the tags with gnis:created or gnis_edited attributes
                elif key =='gnis:created' or key == 'gnis:edited':
                    date = tag.attrib['v']
                    date = audit_dates.clean(date)
                    if not date:
                        continue
                    secondary_tag_dict['value' ] = date
                    secondary_tag_dict['type'] = 'gnis'
                    if tag.attrib['k'] == 'gnis:created':
                        secondary_tag_dict['key'] = 'created'
                    elif tag.attrib['k'] == 'gnis:edited':
                        secondary_tag_dict['key'] = 'edited'

                # The rest of the tags will not be cleaned
                else:
                    secondary_tag_dict['value'] = tag.attrib['v']
                    
                    # If there is a colon, the key is everything after the colon and the type is everything before
                    if COLON.search(key):
                        secondary_tag_dict['key'] = ':'.join(key.split(":")[1:])
                        secondary_tag_dict['type'] = str(key.split(":")[0])
                    else:
                        secondary_tag_dict['key'] = key
                        secondary_tag_dict['type'] = 'regular'

            tags.append(secondary_tag_dict)

        return {'node': node_attribs, 'node_tags': tags}

    # Handle the way elements
    elif element.tag == 'way':
        way_id = element.attrib['id']

        # Handle the information in the top level way element attributes
        for key, value in element.items():
            if key in WAY_FIELDS:
                way_attribs[key] = value

        # Iterate through all the "tag" tags in the way element
        for tag in element.iter('tag'):

            # Pass on any tags with a problem character in the k attribute
            if PROBLEMCHARS.search(tag.attrib['k']):
                continue
            else:
                secondary_tag_dict = {}
                secondary_tag_dict['id'] = way_id
                key = tag.attrib['k']
                secondary_tag_dict['key'] = key

                # Clean the elevation data tags
                if key == 'ele':
                    elevation = tag.attrib['v']
                    elevation = audit_elevation.clean(elevation)
                    if not elevation:
                        continue # Remove the elevation dicts that are not valid
                    secondary_tag_dict['value'] = elevation
                    secondary_tag_dict['type'] = 'regular'

                # Clean the street data tags
                elif key == 'addr:street' or key == 'name':
                    street = tag.attrib['v']
                    street = audit_street_types.clean(street)
                    secondary_tag_dict['value'] = street
                    secondary_tag_dict['type'] = 'regular'

                # Clean the amenity data tags
                elif key == 'amenity':
                    amenity = tag.attrib['v']
                    amenity = audit_amenities.clean(amenity)
                    if not amenity:
                        continue # Remove the amenity dicts that are not valid
                    secondary_tag_dict['value'] = amenity
                    secondary_tag_dict['type'] = 'regular'


                # Clean the dates in the tags with gnis:created or gnis:edited attributes
                elif key =='gnis:created' or key == 'gnis:edited':
                    date = tag.attrib['v']
                    date = audit_dates.clean(date)
                    if not date:
                      continue
                    secondary_tag_dict['value'] = date
                    secondary_tag_dict['type'] = 'gnis'
                    if tag.attrib['k'] == 'gnis:created':
                        secondary_tag_dict['key'] = 'created'
                    elif tag.attrib['k'] == 'gnis:edited':
                        secondary_tag_dict['key'] = 'edited'
    

                # Clean the zip code data tags
                elif 'zip_left' in key:
                    zip_code = tag.attrib['v']
                    zip_code = audit_zip.clean(zip_code)
                    if not zip_code:
                        continue # Remove the zip codes that are not valid
                    secondary_tag_dict['value'] = zip_code
                    secondary_tag_dict['key'] = 'zip_left'
                    secondary_tag_dict['type'] = 'tiger'

                elif 'zip_right' in key:
                    zip_code = tag.attrib['v']
                    zip_code = audit_zip.clean(zip_code)
                    if not zip_code:
                        continue # Remove the zip codes that are not valid
                    secondary_tag_dict['value'] = zip_code
                    secondary_tag_dict['key'] = 'zip_right'
                    secondary_tag_dict['type'] = 'tiger'

                elif 'postcode' in key:
                    zip_code = tag.attrib['v']
                    zip_code = audit_zip.clean(zip_code)
                    if not zip_code:
                        continue # Remove the zip codes that are not valid
                    secondary_tag_dict['value'] = zip_code
                    secondary_tag_dict['key'] = 'postcode'
                    secondary_tag_dict['type'] = 'addr'

                    
                else:
                    # The rest of the tags are not cleaned
                    secondary_tag_dict['value'] = tag.attrib['v']

                    #  If there is a colon, the key is everything after the colon and the type is everything before
                    if COLON.search(key):
                        secondary_tag_dict['key'] = ':'.join(key.split(":")[1:])
                        secondary_tag_dict['type'] = str(key.split(":")[0])
                    #  If there is no colon, the type is regular
                    else:
                        secondary_tag_dict['key'] = key
                        secondary_tag_dict['type'] = 'regular'

            tags.append(secondary_tag_dict)

        # Iterate through the node (nd) tags in the way element
        for i, nd in enumerate(element.iter('nd')):
            way_node_dict = {}
            way_node_dict['id'] = way_id
            way_node_dict['node_id'] = nd.attrib['ref']
            way_node_dict['position'] = i

            way_nodes.append(way_node_dict)

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

    # Handle the information in the relation element
    elif element.tag == 'relation':
        relation_id = element.attrib['id']

        # Handle the information in the top level relation element attributes
        for key, value in element.items():
            if key in RELATION_FIELDS:
                relation_attribs[key] = value

        # Iterate through the member tags and record their attributes
        for i, member in enumerate(element.iter('member')):

            # Create a new dictionary for each member
            relation_member_dict = {}
            relation_member_dict['id'] = relation_id
            relation_member_dict['member_id'] = member.attrib['ref']
            relation_member_dict['type'] = member.attrib['type']
            relation_member_dict['role'] = member.attrib['role']
            relation_member_dict['position'] = i

            relation_members.append(relation_member_dict)

        #  Iterate through all the "tag" tags in the relation element
        for tag in element.iter('tag'):
            # Skip over any tags that have problem characters in their key
            if PROBLEMCHARS.search(tag.attrib['k']):
                continue
            else:
                # Create a new dictionary for each tag
                secondary_tag_dict = {}
                secondary_tag_dict['id'] = relation_id
                key = tag.attrib['k']
                secondary_tag_dict['key'] = key

                # Handle the elevation data tags
                if key == 'ele':
                    elevation = tag.attrib['v']
                    elevation = audit_elevation.clean(elevation)
                    if not elevation:
                        continue # Remove the elevation dicts that are not valid
                    secondary_tag_dict['value'] = elevation
                    secondary_tag_dict['type'] = 'regular'

                # Clean the zip code data tags
                elif 'zip' in key:
                    zip_code = tag.attrib['v']
                    zip_code = audit_zip.clean(zip_code)
                    if not zip_code:
                        continue # Remove the zip codes that are not valid
                    secondary_tag_dict['value'] = zip_code
                    secondary_tag_dict['type'] = 'regular'

                else:
                    # The rest of the tags are not cleaned
                    secondary_tag_dict['value'] = tag.attrib['v']

                    #  If there is a colon, the key is everything after the colon and the type is everything before
                    if COLON.search(key):
                        secondary_tag_dict['key'] = ':'.join(key.split(":")[1:])
                        secondary_tag_dict['type'] = str(key.split(":")[0])
                    #  If there is no colon, the type is regular
                    else:
                        secondary_tag_dict['key'] = key
                        secondary_tag_dict['type'] = 'regular'

            tags.append(secondary_tag_dict)

        return {'relation' : relation_attribs, 'relation_members' : relation_members, 'relation_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.items())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: v for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    # Open files with encoding of UTF-8 to prevent 'b' from being appended to beginning of each data point
    # Rather than writing with encoding of 'UTF-8', open file with that encoding
    with codecs.open(NODES_PATH, 'w', encoding='UTF-8') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w', encoding='UTF-8') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w', encoding='UTF-8') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w', encoding='UTF-8') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w', encoding='UTF-8') as way_tags_file, \
         codecs.open(RELATIONS_PATH, 'w', encoding='UTF-8') as relations_file, \
         codecs.open(RELATION_MEMBERS_PATH, 'w', encoding='UTF-8') as relation_members_file, \
         codecs.open(RELATION_TAGS_PATH, 'w', encoding='UTF-8') as relation_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)
        relations_writer = UnicodeDictWriter(relations_file, RELATION_FIELDS)
        relation_members_writer = UnicodeDictWriter(relation_members_file, RELATION_MEMBERS_FIELDS)
        relation_tags_writer = UnicodeDictWriter(relation_tags_file, RELATION_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()
        relations_writer.writeheader()
        relation_members_writer.writeheader()
        relation_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way', 'relation')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])
                elif element.tag == 'relation':
                    relations_writer.writerow(el['relation'])
                    relation_members_writer.writerows(el['relation_members'])
                    relation_tags_writer.writerows(el['relation_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)
