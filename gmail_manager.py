"""
This module ...
"""
import datetime
import time
import re
from auth_adt import Auth


class GUser:
    """
    Class provides Gmail user's interface.
    """
    def __init__(self):
        """
        Initialize a user inbox
        """
        self.user_id = 'me'
        self.end_date = self.get_end_date()
        self.service = None
        self.set_service()

    @staticmethod
    def get_end_date():
        """
        Return a date that is a month before the today's date
        (eg. "2020-04-07")
        :return: str
        """
        date_now = str(datetime.date.today())
        year, month, day = date_now.split('-')

        if int(month) == 1:
            year = str(int(year) - 1)
            prev_month = '12'
        else:
            prev_month = str(int(month) - 1)

        if len(prev_month) == 1:
            prev_month = '0' + prev_month

        end_date = '-'.join([year, prev_month, day])
        return end_date

    @staticmethod
    def get_message_date(message):
        """
        Returns the message date with special formatting.
        :param message: dict
        :return: string
        """
        iternal_date = int(message["internalDate"][:-3])
        return datetime.datetime.fromtimestamp(iternal_date)

    def set_service(self):
        """
        Return a service got by user's credentials
        :return: None
        """
        authenticator = Auth()
        self.service = authenticator.service

    def get_inbox_info(self):
        """
        Return a dict that has sender as a key and number
        of messages as a value.
        :return: inbox_info = {from (str): value (int), ...}
        """
        user_message_id_lst = self.get_user_messages_lst()
        inbox_info_dict = dict()
        for i in user_message_id_lst:
            sender_email = self.retrieve_sender_info(i["id"])[1]
            if not sender_email:
                break

            if sender_email in inbox_info_dict.keys():
                inbox_info_dict[sender_email] += 1
            else:
                inbox_info_dict[sender_email] = 1
        return inbox_info_dict

    def get_user_messages_lst(self, ladelids=['INBOX']):
        """
        Returns user messages list, which contains only an id and a threadId.
        Additional message details can be fetched
        using the messages.get method.
        :return: list of dict [{'id': '1714f35d4d28e916',
                                'threadId': '1714f35d4d28e916'}, ...]
        """
        results = self.service.users().messages().list(userId=self.user_id,
                                                       labelIds=ladelids,
                                                       maxResults=20).execute()
        # тут треба продумати що буде якшо за ост
        # місяць більше ніж 500 повідомлень
        # print(results)
        messages_lst = results['messages']
        return messages_lst

    def retrieve_sender_info(self, message_id):
        """
        Retrieves such information as name of the sender and its email address.
        :message_id: str
        :return: tuple of str  = ("name", "email")
        """
        time1 = time.time()
        message = self.service.users().messages().get(userId=self.user_id,
                                                      id=message_id,
                                                      format="metadata",
                                                      metadataHeaders=["From"]).execute()
        # print(message)
        time2 = time.time()
        print("new message proceeded, time =", time2 - time1)
        if self.is_valid_date(message):

            sender_email = re.findall("<.*>",
                                      message["payload"]["headers"][0]["value"])[0]
            sender_name = message["payload"]["headers"][0]["value"]
            sender_name = sender_name[:sender_name.index("<")].strip()
            return sender_name, sender_email

        return None

    @staticmethod
    def is_valid_date(message):
        """
        Return True if a message date is bigger than the end date,
        False otherwise
        :return: bool
        """
        return True

    def get_unread_number(self):
        """
        Return a number of unread messages that are up to end date
        :return: int
        """
        pass

    def delete_message(self, service, message_id):
        """
        Delete a certain message by message ID
        :param service:
        :param message_id: str
        """
        service.users().messages().trash(user_id=self.user_id,
                                         id=message_id).execute()

    def unsubscribe(self):
        pass

    def remove_label(self):
        pass


if __name__ == "__main__":

    # testing get_inbox_info() method
    GMAIL_USER = GUser()
    print(GMAIL_USER.get_inbox_info())
