"""
This module implements auth ADT.
"""
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Auth:
    """
    Class provides Gmail user's authentication.
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
              'https://www.googleapis.com/auth/gmail.labels']

    def __init__(self):
        """
        Auth initialization.
        """
        self.service = None
        self.set_service()

    def authorization(self):
        """
        Retruns of credential of a user, in other words authorizes him/her.
        :return: google.oauth2.credentials.Credentials
        """
        creds = None
        # The file token.pickle stores the user's access
        # and refresh tokens, and is
        # created automatically when the authorization
        # flow completes for the first
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
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def set_service(self):
        """
        Sets the value of self.service.
        :return: None
        """
        creds = self.authorization()
        self.service = build('gmail', 'v1', credentials=creds)
