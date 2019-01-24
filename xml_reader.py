import csv
import xml.etree.ElementTree

print("helo")

e = xml.etree.ElementTree.parse('strings.xml').getroot()
print(e.tag)
list_to_add = []
for string in e.findall('string'):
	# print string.get('name') + "," + string.text
	name = string.get('name')
	value = string.text

	str_arr = []
	str_arr.append(name)
	str_arr.append(value)
	list_to_add.append(str_arr)
	
print(len(list_to_add))
# print(list_to_add)
	# print name,',',value
	
