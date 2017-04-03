import xml.etree.cElementTree as ET
import heapq
import mappings

map_file = 'cleveland_ohio.xml'

suspect_elevations = []
bad_elevations = []

elevation_mapping = mappings.elevation_mapping


def audit():
	for _, elem in ET.iterparse(map_file):
		if elem.tag == 'tag':
			if elem.attrib['k'] == 'ele':
				try:
					elevation = int(elem.attrib['v'])
					if elevation > 320 or elevation < 124:
						suspect_elevations.append(elevation)
				except:
					bad_elevations.append(elem.attrib['v'])


def clean(elevation):
	if elevation in elevation_mapping:
		elevation = elevation_mapping[elevation]
	return elevation

bad_elevations = ['318;313', '304.5', '298.4', '679"', '348;352;358']


if __name__=="__main__":
	problem_elevations = ['3', '3', '42', '1188'] + bad_elevations
	for elevation in problem_elevations:
		cleaned_elevation = clean(elevation)
		print("{} --> {}".format(elevation, cleaned_elevation))