import xml.etree.cElementTree as ET
import heapq
import mappings

map_file = 'cleveland_ohio.xml'

s
elevation_mapping = mappings.elevation_mapping




def audit():
	suspect_elevations = []
	invalid_elevations = []

	for _, elem in ET.iterparse(map_file):
		if elem.tag == 'tag':
			if elem.attrib['k'] == 'ele':
				try: # Try to convert the elevation to an integer
					elevation = int(elem.attrib['v'])
					if elevation > 320 or elevation < 124: # Elevation limits in meters identified from the USGS
						suspect_elevations.append(elevation)
				except: #
					invalid_elevations.append(elem.attrib['v'])


def clean(elevation):
	if elevation in elevation_mapping:
		elevation = elevation_mapping[elevation]
	return elevation

invalid_elevations = ['318;313', '304.5', '298.4', '679"', '348;352;358']


if __name__=="__main__":
	problem_elevations = ['3', '3', '42', '1188'] + invalid_elevations
	for elevation in problem_elevations:
		cleaned_elevation = clean(elevation)
		print("{} --> {}".format(elevation, cleaned_elevation))