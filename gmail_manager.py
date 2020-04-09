from datetime import date


class Auth:
    def __init__(self):
        self.service = None

    def authorization(self):
        pass

    def set_service(self):
        pass


class GUser:
    def __init__(self):
        """
        Initialize a user inbox
        """
        self.userId = 'me'
        self.end_date = self.get_end_date()
        self.service = Auth().service

    @staticmethod
    def get_end_date():
        """
        Return a date that is a month before the today's date
        (eg. "2020-04-07")
        :return: str
        """
        date_now = str(date.today())
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

    def get_service(self):
        """
        Return a service got by user's credentials
        :return:
        """
        pass

    def get_inbox_info(self):
        """
        Return a dict that has sender as a key and number of messages as a value
        :return: inbox_info = {from (str): value (int), ...}
        """
        pass

    def get_sender_info(self):
        """
        Return a sender info as <name> <email>
        :return: str
        """
        pass

    def is_valid_date(self):
        """
        Return True if a message date is bigger than the end date,
        False otherwise
        :return: bool
        """
        pass

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
        service.users().messages().trash(userId=self.userId, id=message_id).execute()

    def unsubscribe(self):
        pass

    def remove_label(self):
        pass

