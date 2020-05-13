"""
This module ...
"""
from .auth_adt import Auth
import datetime
import re
import json


class GUser:
    """
    Class provides Gmail user's interface.
    """

    def __init__(self):
        """
        Initialize a user inbox
        """
        self.user_id = 'me'
        self.end_date = None
        self.get_end_date()
        self.today_date = datetime.datetime.today()
        self.service = None
        self.set_service()
        self.label_types = ['UNREAD', 'INBOX', 'CATEGORY_PERSONAL', 'CATEGORY_SOCIAL',
                            'CATEGORY_PROMOTIONS', 'CATEGORY_UPDATES', 'CATEGORY_FORUMS']
        self.categories_info_dict = dict()
        self.messages_by_category_dict = dict()
        self.unread_info_dict = dict()
        self.get_categories_info()
        self.get_unread_info()

    def set_service(self):
        """
        Return a service got by user's credentials
        :return: None
        """
        authenticator = Auth()

        self.service = authenticator.service

    def get_end_date(self):
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

        end_date = datetime.datetime(int(year), int(prev_month), int(day))
        self.end_date = end_date

    @staticmethod
    def get_message_date(message):
        """
        Returns the message date with special formatting.
        :param message: dict
        :return: string
        """
        internal_date = int(message["internalDate"][:-3])
        return datetime.datetime.fromtimestamp(internal_date)

    def get_inbox_info(self, ladelid='CATEGORY_PERSONAL'):
        """
        Return a dictionary that has sender as a key and number
        of messages as a value.
        :return: inbox_info = {from (str): value (int), ...}
        """
        user_message_id_lst = self.messages_by_category_dict[ladelid]
        inbox_info_dict = dict()
        sender_message_id_set = set()
        label_message_id_set = set()
        for i in user_message_id_lst:
            label_message_id_set.add(i["id"])

        while label_message_id_set:
            sender_info = self.retrieve_sender_info(next(iter(label_message_id_set)))
            # tuple:(sender_email, sender_name)
            if not sender_info:
                print("There is an error in retrieving sender info")
                break
            sender_email = sender_info[0]
            sender_message_id_lst = self.get_user_messages_lst(ladelid, sender_email)
            for i in sender_message_id_lst:
                sender_message_id_set.add(i["id"])
            if sender_email in inbox_info_dict.keys():
                inbox_info_dict[sender_email] += 1
            else:
                inbox_info_dict[sender_email] = len(sender_message_id_set)
            label_message_id_set = label_message_id_set - sender_message_id_set
        return inbox_info_dict

    def get_inbox_info_old(self):
        """
        Return a dictionary that has sender as a key and number
        of messages as a value.
        :return: inbox_info = {from (str): value (int), ...}
        """
        user_message_id_lst = self.get_user_messages_lst(ladelids='CATEGORY_PERSONAL')
        inbox_info_dict = dict()
        for i in user_message_id_lst:
            sender_email = self.retrieve_sender_info(i["id"])
            if not sender_email:
                print("There is an error in retrieving sender info")
                break
            sender_email = sender_email[0]
            if sender_email in inbox_info_dict.keys():
                inbox_info_dict[sender_email] += 1
            else:
                inbox_info_dict[sender_email] = 1
        return inbox_info_dict

    def get_user_messages_lst(self, ladelids='INBOX', sender_email=None):
        """
        Returns user messages list on the last 30 days,
        which contains only an id and a threadId.
        Additional message details can be fetched
        using the messages.get method.
        :return: list of dict [{'id': '1714f35d4d28e916',
                                'threadId': '1714f35d4d28e916'}, ...]
        """
        timestamp_after = int(self.end_date.timestamp())  # timestamp of start day
        timestamp_before = int(self.today_date.timestamp())  # timestamp of start day + 30 days

        if sender_email:
            query = f"from:({sender_email}) after:{timestamp_after} before:{timestamp_before}"
        else:
            query = f"after:{timestamp_after} before:{timestamp_before}"
        results = self.service.users().messages().list(userId=self.user_id,
                                                       labelIds=ladelids,
                                                       maxResults=500, q=query).execute()

        # print(results)
        messages_lst = results['messages']
        return messages_lst

    def retrieve_sender_info(self, message_id):
        """
        Retrieves such information as name of the sender and its email address.
        :message_id: str

        :return: tuple of str  = ("name", "email")
        """
        # time1 = time.time()
        message = self.service.users().messages().get(userId=self.user_id,
                                                      id=message_id,
                                                      format="metadata",
                                                      metadataHeaders=["From"]).execute()
        # time2 = time.time()
        # print("new message proceeded, time =", time2 - time1)

        if self.is_valid_date(message):
            try:
                sender_email = re.findall("<.*>",
                                          message["payload"]["headers"][0]["value"])[0]
            except IndexError:
                sender_email = message["payload"]["headers"][0]["value"]
            sender_name = message["payload"]["headers"][0]["value"]
            if sender_name != sender_email:
                sender_name = sender_name[:sender_name.index("<")].strip()
            return sender_name, sender_email

        return None

    def is_valid_date(self, message):
        """
        Return True if a message date is bigger than the end date,
        False otherwise
        :return: bool
        """

        return GUser.get_message_date(message) > self.end_date

    def get_categories_info(self):
        """
        Create (dict) messages_by_category_dict = {"Primary": list
        of messages, "Updates": list, "Promotions": list}
        Create (dict) categories_info_dict = {"Primary": num,
        "Updates": num, "Promotions": num}
        """
        for i in self.label_types:
            messages_category_lst = self.get_user_messages_lst(i)
            self.categories_info_dict[i] = len(messages_category_lst)
            self.messages_by_category_dict[i] = messages_category_lst

    def get_unread_info(self):
        """
        Return a number of unread messages and read messages that are up to end date.
        Create (dict) unread_info_dict = {"READ": num_all - num_unread, "UNREAD": num}
        """
        unread_label = 'UNREAD'
        read_label = 'READ'
        self.unread_info_dict[unread_label] = self.categories_info_dict[unread_label]
        self.unread_info_dict[read_label] = self.categories_info_dict["INBOX"] \
                                            - self.unread_info_dict[unread_label]

    def delete_message(self, message_id):
        """
        Delete a certain message by message ID

        :param message_id: str
        """
        self.service.users().messages().trash(user_id=self.user_id,
                                              id=message_id).execute()

    @staticmethod
    def write_json(inbox_info_dict):
        """
        This function loads the data from the dictionary to json file.
        Namely, it loads the data got from GUser.get_inbox_info method.
        :param inbox_info_dict: dict
        :return: None
        """
        with open("output_data_examples.inbox_info.json", 'w') as json_file:
            json.dump(inbox_info_dict, json_file, indent=4, ensure_ascii=False)
