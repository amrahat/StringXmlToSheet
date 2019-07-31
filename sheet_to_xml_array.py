from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import codecs

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1HCc9z-BUSPeZNMKWVW39ag_Vm0mIoBbY-qXcSLv-kmA'
SAMPLE_RANGE_NAME = 'food_event!B4:CD23'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    service = authenticate()

    get_bangla_in_xml(service)
    # get_nepali_in_xml(service)


def authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    return service


def get_strings_in_xml(service, range, key_index, value_index, file_name):
    result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                 range=range).execute()
    values = result.get('values', [])

    root = ET.Element("resources")
    current_array = ""
    element = ET.Element("string-array")
    if not values:
        print('No data found.')
    else:
        for row in values:
            print(row[key_index].strip())
            print("current: "+current_array)

            if current_array != row[key_index].strip():
                element = ET.SubElement(root, "string-array", name=row[key_index].strip())
                ET.SubElement(element, "item").text = row[value_index].strip()
                current_array = row[key_index].strip()
            else:
                ET.SubElement(element, "item").text = row[value_index].strip()

        # print(row[value_index].strip())
        # ET.SubElement(root, "string", name=row[key_index].strip()).text = row[value_index].strip()

    tree = ET.ElementTree(root)
    xmlstr = minidom.parseString(ET.tostring(root, )).toprettyxml(indent="   ")
    with codecs.open(file_name, "w", "utf-8") as f:
        f.write(xmlstr)

    print("Data saved in " + file_name)


def get_bangla_in_xml(service):
    range = 'food_event!B4:CD23'
    key_index = 0
    value_index = 2
    get_strings_in_xml(service, range, key_index, value_index, "array_output.xml")


def get_nepali_in_xml(service):
    range = 'MXD!B4:E16'
    key_index = 0
    value_index = 3
    get_strings_in_xml(service, range, key_index, value_index, "nepali_mxd.xml")


if __name__ == '__main__':
    main()
