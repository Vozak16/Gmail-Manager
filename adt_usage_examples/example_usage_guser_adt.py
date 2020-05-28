from my_charts import GUser
import time
import urlfetch

def main():
    """
    Show the example of work of Gmail Manager ADT
    :return: None
    """
    GMAIL_USER = GUser()
    print("Dictionary shows the quantity of read and"
          " unread messages during the last 30 days.")
    print(GMAIL_USER.unread_info_dict)
    print()

    print("Dictionary shows the quantity of messages for each"
          " category during the last 30 days.")
    print(GMAIL_USER.categories_info_dict)
    print()

    print(GMAIL_USER.label_types)
    chosen_category = input("Please choose and enter the category from the list above, "
                            "you want to get more detailed information about senders:")
    print("Please, wait :)")
    print()
    time1 = time.time()
    senders_dict = GMAIL_USER.get_inbox_info(chosen_category)
    time2 = time.time()
    print("get_inbox_info proceeded, time =", time2 - time1)
    time1 = time.time()
    senders_sub_dict = GMAIL_USER.get_subscription_info()
    time2 = time.time()
    print("get_inbox_info proceeded, time =", time2 - time1)
    print("Dictionary above shows the quantity of messages for each"
          " senders in the category {} during the last 30 days.".format(chosen_category))
    print(senders_dict)
    print("The total amount of senders in the category {}:".format(chosen_category),
          len(senders_dict))
    print("Dictionary above shows the messages info for each"
          " senders, who you can unsubscribe from, in the category {} during the last 30 days.".format(chosen_category))
    print(senders_sub_dict)
    print("Dictionary above shows the quantity of messages for each"
          " senders in the category {} during the last 30 days.".format(chosen_category))
    print(GMAIL_USER.get_chart_inbox_info())
    print("List above shows the senders, who you can unsubscribe from,"
          "in the category {} during the last 30 days.".format(chosen_category))
    print(GMAIL_USER.get_lst_sender_sub())


    """
    if senders_sub_dict:
        # Unsubscribe
        sender = input("Choose a sender to unsubscribe from: ")
        try:
            url = senders_sub_dict[sender]['sub_url']
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
            print("Done!")"""
    """senders_dict = GMAIL_USER.get_inbox_info_old()
    print(senders_dict)
    print(len(senders_dict))"""




if __name__ == '__main__':
    main()
