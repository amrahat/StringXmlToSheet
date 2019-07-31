from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv
import xml.etree.ElementTree
import sys

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1HCc9z-BUSPeZNMKWVW39ag_Vm0mIoBbY-qXcSLv-kmA'


def get_list_to_add(filename, include_key):
    e = xml.etree.ElementTree.parse(filename).getroot()
    print(e.tag)
    list_to_add = []
    for string in e.findall('string'):
        # print string.get('name') + "," + string.text
        name = string.get('name')
        value = string.text

        str_arr = []
        if include_key:
            str_arr.append(name)
        str_arr.append(value)
        list_to_add.append(str_arr)

    print(len(list_to_add))
    return list_to_add


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

    try:
        string_file_name = sys.argv[1]
    except IndexError as e:
        string_file_name = None

    print(string_file_name)

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

    # Call the Sheets API
    sheet = service.spreadsheets()

    values = []

    try:
        values = get_list_to_add(string_file_name, True)
        # values.insert(0,["Key","Value"])

        update_range = "new_sprint!B4:C" + str(4 + len(values))
        update(values, service, update_range)
    except IOError as e:
        print("No such file found")


def update(values, service, update_range):
    print(len(values))
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=update_range,
                                                    valueInputOption="RAW", body=body).execute()

    print('{0} cells updated ok.'.format(result.get('updatedCells')))


if __name__ == '__main__':
    main()
