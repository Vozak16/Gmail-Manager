from .auth_adt import Auth
from apiclient import errors
import urlfetch
import base64
import re


class GUnsubscribe:
    def __init__(self):
        """
        Initialize a service
        """
        self.service = Auth().service
        self.seen = set()
        self.sub_info = dict()

    def get_message(self, msg_id):
        """
        Get the full email message data with body content in the raw field as a base64url.
        Decode this message and
        Return a raw message

        :param msg_id: str
        :return: message
        """
        try:
            message = self.service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII')).decode('utf-8', 'ignore')
            return msg_str
        except errors.HttpError as error:
            print('An error occurred getting a message: %s' % error)

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

    @staticmethod
    def get_sender(msg_str):
        """
        Return a sender name

        :param msg_str: str
        :return: str
        """
        pattern = re.compile(r"(?<=From: )(.*)")
        match = pattern.search(msg_str)
        if match:
            return match.group(0)
        return None

    def get_subscription_info(self, category):
        """
        Update a dictionary. sub_info = {<sender_name>: {
                                                'sub_url': str,
                                                'msg_ids': list(str, ...)
                                                }, ...}

        :param category: (str) category of the mailbox (e.g. "CATEGORY_PROMOTIONS")
        """
        results_ = self.service.users().messages().list(userId='me', labelIds=[category]).execute()
        messages = results_.get('messages')

        for msg in messages:
            msg_id = msg['id']
            msg_str = self.get_message(msg_id)

            try:
                unsubscribe_urls = self.get_unsubscribe_url(msg_str)
                http_url = self.get_http_url(unsubscribe_urls)
            except AttributeError:
                continue

            if not http_url:
                continue

            sender = self.get_sender(msg_str).split(' <')[0]
            if sender not in self.seen:

                self.sub_info[sender] = {
                    'sub_url': http_url,
                    'msg_ids': [msg_id]
                }
                self.seen.add(sender)
            else:
                self.sub_info[sender]['msg_ids'].append(msg_id)

    def unsubscribe(self, sender):
        """
        Unsubscribe from a certain sender by his/her unsubscribe url.

        :param sender: str
        """
        try:
            url = self.sub_info[sender]['sub_url']
            response = urlfetch.get(url)
            print(response.status)
        except urlfetch.UrlfetchException:
            print('Unsubscribe timeout exceeded!')

    def delete_messages(self, sender):
        """
        Delete all messages from a certain sender.

        :param sender: str
        """
        messages = self.sub_info[sender]['msg_ids']
        for msg_id in messages:
            self.service.users().messages().trash(userId='me', id=msg_id).execute()
