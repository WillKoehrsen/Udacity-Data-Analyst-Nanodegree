import xml.etree.cElementTree as ET
import mappings

map_file = 'cleveland_ohio.xml'
source_file = 'amenitiesSource.xml'

# The keys will be the amenities and the value the number of times in appears
count_amenities = dict()

amenities_mapping = mappings.amenities_mapping

def audit():
	# Iterate through the osm file
	for _ , elem in ET.iterparse(map_file):
		# Iterate through all the tags named tag
		for entry in elem.iter('tag'):
			# Find the amenity attributes
			if entry.attrib['k'] == 'amenity':
				amenity = entry.attrib['v']
				# Count the number of times each amenity appears in the data
				# If amenity is not in dictionary, start counting at one
				# If the amenity is in the dictionary, increment the count
				count_amenities[amenity] = count_amenities.get(amenity, 0) + 1

	# Create a tree for parsing the XML from the webpage
	source_tree = ET.parse(source_file)
	source_root = source_tree.getroot()

	# The list of verified amenities will be a set of unique names
	amenities_from_source = set()

	# Table class has been identified from inspection of HTML
	for table in source_root.iter('table'):
		if table.attrib['class'] == 'wikitable':
			for row in table:
				#Iterate through the data in each row of the table
				for data in row:
					for element in data:
						if element.tag == 'a':
							if element.text:
								amenities_from_source.add(element.text.strip())

	# Identify the amenities in the map not verified on the openstreetmap website
	non_verified_amenities = dict()

	for key in count_amenities:
		if key not in amenities_from_source:
			# If key is not in dictionary, start counting at one
			# If the key is in the dictionary, increment the count
			non_verified_amenities[key] = non_verified_amenities.get(key, 0) + 1

def clean(amenity):
	if amenity in amenities_mapping:
		amenity = amenities_mapping[amenity]
	return amenity
