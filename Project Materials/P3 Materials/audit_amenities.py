import xml.etree.cElementTree as ET
from collections import defaultdict

filename = 'cleveland_ohio.xml'
source_file = 'amenitiesSource.xml'

count_types = {'node': 0 , 'way': 0, 'relation' :0}
count_amenities = {}

for _ , elem in ET.iterparse(filename):
	tag = elem.tag
	if tag == 'node':
		for entry in elem.iter('tag'):
			if entry.attrib['k'] == 'amenity':
				amenity = entry.attrib['v']
				if amenity not in count_amenities.keys():
					count_amenities[amenity] = 1
				else:
					count_amenities[amenity] += 1


amenities_from_source = set()
for _, elem in ET.iterparse(source_file):
	tag = elem.tag
	if tag == 'table':
		if elem.attrib['class'] == 'wikitable':
			for a in elem.iter('a'):
				if a.text:
					amenity = a.text.strip()
					amenities_from_source.add(amenity)

print(amenities_from_source)

for key in count_amenities:
	if key not in amenities_from_source:
		print(key)