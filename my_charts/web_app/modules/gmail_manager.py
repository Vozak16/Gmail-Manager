"""
This module ...
"""
from .auth_adt import Auth
import datetime
import re
import time
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
        self.label_types = [('UNREAD', 'Unread'), ('INBOX', 'Inbox'),
                            ('CATEGORY_PERSONAL', 'Primary'),
                            ('CATEGORY_SOCIAL', 'Social'),
                            ('CATEGORY_PROMOTIONS', 'Promotions'),
                            ('CATEGORY_UPDATES', 'Updates'),
                            ('CATEGORY_FORUMS', 'Forums')]
        self.defined_categories = ['Primary', 'Social',
                                   'Promotions', 'Updates']
        self.categories_info_dict = dict()
        self.defined_categories_info_dict = dict()
        self.messages_by_category_dict = dict()
        self.unread_info_dict = dict()
        self.get_categories_info()
        self.get_unread_info()
        self.get_defined_categories_info()

    def get_defined_categories_info(self):
        """
        Create (dict) defined_categories_info_dict =
        {"Primary": num, 'Social':num,
        "Updates": num, "Promotions": num}
        :return: None
        """
        for i in self.defined_categories:
            self.defined_categories_info_dict[i] = self.categories_info_dict[i]

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
        :return: inbox_info = {from (str): tuple(value (int),
        sender_name, sender_msg_id), ...}
        """
        user_message_id_lst = self.messages_by_category_dict[ladelid]
        inbox_info_dict = dict()
        sender_message_id_set = set()
        label_message_id_set = set()
        for i in user_message_id_lst:
            label_message_id_set.add(i["id"])
        senders_num = 0
        total_time = 0
        msg_num = 0
        while label_message_id_set:
            sender_info = self.retrieve_sender_info(next(iter(label_message_id_set)))
            # tuple:(sender_email, sender_name)
            if not sender_info:
                print("There is an error in retrieving sender info")
                break
            try:
                sender_email = sender_info[1]
            except KeyError:
                sender_email = sender_info[0]
            time1 = time.time()
            sender_message_id_lst = self.get_user_messages_lst(ladelid, sender_email)
            time2 = time.time()
            total_time += time2 - time1
            # print("new message proceeded, time =", time2 - time1)

            senders_num += 1
            for i in sender_message_id_lst:
                sender_message_id_set.add(i["id"])
            if sender_email in inbox_info_dict.keys():
                print('Something go wrong')
                inbox_info_dict[sender_email] += 1
            else:
                inbox_info_dict[sender_email] = (len(sender_message_id_set),
                                                 sender_info[0], next(iter(sender_message_id_set)))
            label_message_id_set = label_message_id_set - sender_message_id_set
            msg_num += len(sender_message_id_set)
            sender_message_id_set.clear()

        print('senders=', senders_num)
        print('total time', total_time)
        print('messages_category', msg_num)
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
        try:
            messages_lst = results['messages']
        except KeyError:
            return []
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
        Create (dict) messages_by_category_dict = {"Unread": list,
        "Inbox": list,"Primary": list, "Social": list,
        "Promotions": list, "Updates": list, "Forums": list}
        Create (dict) categories_info_dict = {"Unread": int, "Inbox": int,
        "Primary": int, "Social": int, "Promotions": int, "Updates": int,
        "Forums": int}
        :return None
        """
        for i in self.label_types[:6]:
            messages_category_lst = self.get_user_messages_lst(i[0])
            self.categories_info_dict[i[1]] = len(messages_category_lst)
            self.messages_by_category_dict[i[0]] = messages_category_lst

    def get_unread_info(self):
        """
        Return a number of unread messages and read messages that are up to end date.
        Create (dict) unread_info_dict = {"Read": num_all - num_unread, "Unread": num}
        :return None
        """
        unread_label = 'Unread'
        read_label = 'Read'
        self.unread_info_dict[unread_label] = self.categories_info_dict[unread_label]
        self.unread_info_dict[read_label] = self.categories_info_dict["Inbox"] \
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
