from .gmail_manager import GUser


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
    print("Please, wait from 5 to 10 seconds")
    print()
    senders_dict = GMAIL_USER.get_inbox_info()
    print("Dictionary above shows the quantity of messages for each"
          " senders in the category {} during the last 30 days.".format(chosen_category))
    print(senders_dict)
    print("The total amount of messages in the category {}:".format(chosen_category),
          len(senders_dict))


if __name__ == '__main__':
    main()
