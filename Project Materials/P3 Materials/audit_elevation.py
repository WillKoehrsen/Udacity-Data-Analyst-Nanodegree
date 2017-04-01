import xml.etree.cElementTree as ET

map_file = 'cleveland_ohio.xml'

elevations = []
bad_elevations = []

for _, elem in ET.iterparse(map_file):
	if elem.tag == 'tag':
		if elem.attrib['k'] == 'ele':
			try:
				elevation = int(elem.attrib['v'])
				elevations.append(elevation)
			except:
				bad_elevations.append(elem.attrib['v'])

print(max(elevations))