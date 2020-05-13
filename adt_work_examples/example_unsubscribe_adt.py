from program_modules.unsubscribe import GUnsubscribe
import urlfetch


def main():
    """
    Show the example of work of Unsubscribe ADT
    :return: None
    """
    sender_info = GUnsubscribe()
    sender_info.get_subscription_info('CATEGORY_PROMOTIONS')
    mail_info_dict = sender_info.sub_info
    print("Subscription Info: \n")
    print(mail_info_dict)

    if mail_info_dict:
        # Unsubscribe
        sender = input("Choose a sender to unsubscribe from: ")
        try:
            url = mail_info_dict[sender]['sub_url']
            response = urlfetch.get(url)
            print(response.body)
        except KeyError:
            print("Such sender does not exist!")
        else:
            print("Done!")

        # Delete messages
        sender = input("Choose a sender to delete his/her messages: ")
        try:
            sender_info.delete_messages(sender)
        except KeyError:
            print("Such sender does not exist!")
        else:
            print("Done!")


if __name__ == '__main__':
    main()
