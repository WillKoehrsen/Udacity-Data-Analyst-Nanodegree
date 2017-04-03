import xml.etree.cElementTree as ET
import re
import datetime
map_file = 'smallSample.xml'

dates_to_change = []

def audit():
	for _, elem in ET.iterparse(map_file):
		for tag in elem.iter('tag'):
			if tag.attrib['k'] =='gnis:created' or tag.attrib['k'] == 'gnis:edited':
				date = tag.attrib['v']
				try:
					date = datetime.datetime.strptime(date, '%Y-%m-%d')
				except:
					dates_to_change.append(date)

	return dates_to_change

audit()



def clean(date):
	try:
		date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
		return date
	except:
		try:
			date = datetime.datetime.strptime(date, '%m/%d/%Y').date()
			return date.strftime('%Y-%m-%d')
		except:
			return ''

if __name__=="__main__":
	dates_to_change = audit()
	for date in dates_to_change:
		print(clean(date))