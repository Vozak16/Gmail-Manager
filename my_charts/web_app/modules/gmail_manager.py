"""
This module ...
"""
from .auth_adt import Auth
from apiclient import errors
import urlfetch
import base64
import datetime
import re
import time
import json
import ssl
import certifi


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
        self.defined_categories = ['Primary', 'Promotions',
                                   'Updates', 'Social']
        self.categories_info_dict = dict()
        self.defined_categories_info_dict = dict()
        self.messages_by_category_dict = dict()
        self.unread_info_dict = dict()
        self.sub_info = dict()
        self.inbox_info = dict()
        self.chart_inbox_info = dict()
        self.lst_sender_sub = list()
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
            self.defined_categories_info_dict[i] = \
                self.categories_info_dict[i]

    def set_service(self):
        """
        Return a service got by user's credentials
        :return: None
        """
        authenticator = Auth()

        self.service = authenticator.service
        authenticator.delete_token() # delete token.pickle file

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

    def get_inbox_info(self, ladelid='INBOX'):
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
                                                 sender_info[0], next(iter(sender_message_id_set)),
                                                 list(sender_message_id_set))
            label_message_id_set = label_message_id_set - sender_message_id_set
            msg_num += len(sender_message_id_set)
            sender_message_id_set.clear()

        print('senders=', senders_num)
        print('total time', total_time)
        print('messages_category', msg_num)
        self.inbox_info = inbox_info_dict
        self.get_subscription_info()
        self.get_chart_inbox_info()
        self.get_lst_sender_sub()
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

    def get_raw_message(self, msg_id):
        """
        Get the full email message data with body content in the raw field as a base64url.
        Decode this message and
        Return a raw message

        :param msg_id: str
        :return: str
        """
        try:
            message = self.service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII')).decode('utf-8', 'ignore')
            return msg_str
        except errors.HttpError as error:
            print('An error occurred getting a message: %s' % error)

    def get_subscription_info(self):
        """
        Update a dictionary. sub_info = {<sender_name>: {
                                                'sub_url': str,
                                                'msg_ids': list(str, ...)
                                                }, ...}
        """
        senders_sub_num = 0
        for value_tupl in self.inbox_info.values():
            msg_str = self.get_raw_message(value_tupl[2])

            try:
                unsubscribe_urls = self.get_unsubscribe_url(msg_str)
                http_url = self.get_http_url(unsubscribe_urls)
            except AttributeError:
                print('ka')
                continue

            if not http_url:
                continue

            sender = value_tupl[1]
            senders_sub_num += 1

            self.sub_info[sender] = {
                'sub_url': http_url,
                'msg_ids': value_tupl[3]
            }
        print(senders_sub_num)
        return self.sub_info

    @staticmethod
    def get_unsubscribe_url(msg_str):
        """
        Return a list of <mailto: link> and <https: link>

        :param msg_str: str
        :return: str
        """
        pattern = re.compile(r"(?<=List-Unsubscribe: <)(.*)(?=>)")
        match = pattern.search(msg_str)
        if match:
            return match.group(0)
        return None

    @staticmethod
    def get_http_url(urls):
        """
        Return http unsubscribe url if it exists,
        else return None

        :param urls: list(str, str)
        :return: str
        """
        url_list = urls.split('>, <')
        for url in url_list:
            pattern = re.compile(r"http(s)?:.*")
            match = pattern.search(url)
            if match:
                return url
        return None

    def unsubscribe(self, sender):
        """
        Unsubscribe from a certain sender by his/her unsubscribe url.

        :param sender: str
        """
        ctx = ssl.create_default_context(cafile=certifi.where())
        try:
            url = self.sub_info[sender]['sub_url']
            response = urlfetch.get(url)
            print(response.status)
        except urlfetch.UrlfetchException:
            print('Unsubscribe timeout exceeded!')

    def get_chart_inbox_info(self):
        """
        Transforms self.inbox_info to dictionary in
        special format for chart in web page.
        :return: dict
        """
        for i in self.inbox_info.values():
            self.chart_inbox_info[i[1]] = i[0]
        return self.chart_inbox_info

    def get_lst_sender_sub(self):
        """
        Transforms self.sub_info to list with only names
        of the senders, from whom GUser can unsubscribe.
        :return: list
        """
        for i in self.sub_info.keys():
            self.lst_sender_sub.append(i)
        if len(self.lst_sender_sub) >= 8:
            self.lst_sender_sub = self.lst_sender_sub[:7]
        return self.lst_sender_sub

    def delete_messages(self, sender):
        """
        Delete all messages from a certain sender.

        :param sender: str
        """
        messages = self.sub_info[sender]['msg_ids']
        for msg_id in messages:
            self.service.users().messages().trash(userId='me', id=msg_id).execute()

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
