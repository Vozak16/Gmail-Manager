from gmail_manager import GUser
import time

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
    print("Dictionary above shows the quantity of messages for each"
          " senders in the category {} during the last 30 days.".format(chosen_category))
    print(senders_dict)
    print("The total amount of senders in the category {}:".format(chosen_category),
          len(senders_dict))
    """senders_dict = GMAIL_USER.get_inbox_info_old()
    print(senders_dict)
    print(len(senders_dict))"""



if __name__ == '__main__':
    main()
