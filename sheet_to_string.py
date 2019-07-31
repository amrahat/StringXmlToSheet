# 1NzJZgQiPO7wnEH8O2sGyWRSzs8KmsNlamGttBZRtk6U
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

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1NzJZgQiPO7wnEH8O2sGyWRSzs8KmsNlamGttBZRtk6U'


# SAMPLE_SPREADSHEET_ID = '1HCc9z-BUSPeZNMKWVW39ag_Vm0mIoBbY-qXcSLv-kmA'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    service = authenticate()
    get_bangla_in_xml(service)


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
    f = open("demofile.txt", "a")
    root = ET.Element("resources")

    if not values:
        print('No data found.')
    else:
        for row in values:
            if len(row) == 1:
                print(row[0].strip())
                varName = row[0].strip()
                varNameUnderScore = varName.replace(" ", "_").upper()

                f.write("String "+varNameUnderScore+" = \""+row[0].strip()+"\";\n")

        # ET.SubElement(root, "string", name=row[key_index].strip()).text = row[value_index].strip()

    # tree = ET.ElementTree(root)
    # xmlstr = minidom.parseString(ET.tostring(root, )).toprettyxml(indent="   ")
    # with codecs.open(file_name, "w", "utf-8") as f:
    #     f.write(xmlstr)
    #
    # print("Data saved in " + file_name)


def get_bangla_in_xml(service):
    range = 'Drive App!B3:B'
    key_index = 0
    value_index = 2
    get_strings_in_xml(service, range, key_index, value_index, "bangla_vsi.xml")


if __name__ == '__main__':
    main()
