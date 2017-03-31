import xml.etree.cElementTree as ET

filename = 'smallSample.xml'

count_types = {'node': 0 , 'way': 0, 'relation' :0}
count_amenities

for _ , elem in ET.iterparse(filename):
	tag = elem.tag
	if tag == 'node':
		for entry in elem.iter('tag'):
			if entry.attrib['k'] == 'amenity':
				print(entry.attrib['v'])



