import xml.etree.cElementTree as ET
import re
import mappings 

map_file = 'cleveland_ohio.xml'
cleveland_zip_codes = mappings.cleveland_zip_codes
zip_codes = set()
bad_zips = []
suspect_zip_codes = []

def audit():
	for _, elem in ET.iterparse(map_file):
		if elem.tag == 'tag':
			if 'zip' in elem.attrib['k'] or 'postcode' in elem.attrib['k']:
				zip = elem.attrib['v']
				try:
					zip_codes.add(int(zip))
				except:
					bad_zips.append(zip)

	for zip_code in zip_codes:
		if zip_code not in cleveland_zip_codes:
			suspect_zip_codes.append(zip_code)


def clean(zip_code):
	# Easiey way to separate out the problem zip codes
	if len(zip_code) > 5:
		# Regular expression splits the code on ; : - 
		zip_code = re.split('[;:-]', zip_code)
		try:
			if int(zip_code[0]) in cleveland_zip_codes:
				zip_code = zip_code[0]
			elif int(zip_code[-1]) in cleveland_zip_codes:
				zip_code = zip_code[-1]
			else:
				zip_code = ''
		except:
			zip_code = zip_code[0].split(" ")
			if int(zip_code[-1]) in cleveland_zip_codes:
				zip_code = zip_code[-1]
			else:
				zip_code = ''
	else:
		try:
			if int(zip_code) not in cleveland_zip_codes:
				zip_code = ''
		except:
			zip_code = ''# Returning an empty string will drop the tag entirely
	return zip_code

