import xml.etree.ElementTree as et
import xml.etree.ElementTree
from pykml import parser

kml_file = "gulshan_less_zone.kml"
import json

data = []
# e = xml.etree.ElementTree.parse(").getroot()
# for child in e:
#     print child.tag

with open(kml_file) as f:
    # doc = parser.parse(f)
    # print doc.getroot().Document.name
    folder = parser.parse(f).getroot().Document
    i = 1
    for pm in folder.Placemark:
        coordinatesString = str(pm.Polygon.outerBoundaryIs.LinearRing.coordinates)
        if len(coordinatesString) == 0:
            continue
        # print(coordinatesString)
        coordinates = coordinatesString.strip().split()
        # print coordinates
        # print len(coordinates)
        value = {}
        value["id"] = i
        value["name"] = "Gulshan-" + str(i)
        multiples = {}
        multiples['combined_boost_surge_pc'] = i * 5
        boost_time = ["12:00PM", "3:00PM"]
        multiples['boost_time'] = boost_time

        value['multiples'] = multiples

        latlngs = []

        for coord in coordinates:
            coords = coord.split(",")
            latlng = [float(coords[0]), float(coords[1])]
            latlngs.append(latlng)
        latlngs_list = [latlngs]
        value['coordinates'] = latlngs_list
        data.append(value)
        i += 1
        # for child in pm.LineString:
        #     print child.name

    print json.dumps(data)
