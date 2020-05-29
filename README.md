![](https://img.shields.io/github/license/Vozak16/Gmail-Manager)
![](https://img.shields.io/github/commit-activity/w/Vozak16/Gmail-Manager)
![](https://img.shields.io/github/last-commit/Vozak16/Gmail-Manager)
![](https://img.shields.io/github/languages/code-size/Vozak16/Gmail-Manager)
# Gmail_Manager
> First CS year coursework

![](https://github.com/Vozak16/Gmail-Manager/blob/master/Gmail-Manager-Preview.png)

## Table of contents
* [Description](#Description)

* [Input and Output data](#Input-and-Output-Data)

* [Installation and usage](#Installation-and-usage)

* [Usage examples](#Usage-examples)

* [Contributing](#Contributing)

* [Credits](#Credits)

* [Licence](#Licence)

## Description: 
Gmail-Manager is a web-application, which helps Gmail users to analyze and manage subscriptions in their mail inbox, delete the messages from the specific sender. 
In the web application user can:
* Register with his/her gmail inbox and gives permission to view and modify his/her email.
* View and analyze the quantity of messages in the pre-defined categories:'Promotions', 'Updates', 'Social' from the last 30 days.
* View and analyze the quantity of messages in the pre-defined categories:'Read', 'Unread' from the last 30 days.
* Choose one of the pre-defined categories:'Promotions', 'Updates', 'Social' to  view and analyze the quantity of messages in this category by each sender from the last 30 days.
* Choose one of the pre-defined categories:'Promotions', 'Updates', 'Social' to delete all the messages in this category from the specific sender from the last 30 days.
* Choose one of the pre-defined categories:'Promotions', 'Updates', 'Social' to unsubscribe from the specific sender, whose messages belongs to this category.

## Input and Output data:
All the data was loaded with one kind of API:
* [Gmail API]
(https://developers.google.com/gmail/api)


## Installation and usage: 

```bash
$ git clone https://github.com/Vozak16/Gmail-Manager
$ cd Gmail-Manager
$ pip install -r requirements.txt
$ cd my_charts
$ python3 manage.py runserver
```

## Usage examples:

First step is to log in with your Gmail account. User follow the two next steps.
![](https://github.com/Vozak16/Gmail-Manager/blob/master/usage_examples/user_registraion_part1.png)
![](https://github.com/Vozak16/Gmail-Manager/blob/master/usage_examples/user_registraion_part2.png)

User moves to the page Get Started and press the "GET STARTED" button
![](https://github.com/Vozak16/Gmail-Manager/blob/master/usage_examples/get_started_1page.png)

After pressing the "GET STARTED" button user will see the following page with the quantity of messages in the pre-defined categories:'Read', 'Unread', Promotions', 'Updates', 'Social' from the last 30 days.
![](https://github.com/Vozak16/Gmail-Manager/blob/master/usage_examples/read_unread_messages_page2.png)
![](https://github.com/Vozak16/Gmail-Manager/blob/master/usage_examples/messages_by_main_categories_page2.png)

Then user be pressing the specific category button in the menu on page's left can view and analyze the quantity of messages in this category by each sender from the last 30 days.
![](https://github.com/Vozak16/Gmail-Manager/blob/master/usage_examples/messages_by_sender_page3.png)

## Contributing: 

If you want to contribute in one way or another, open an issue or clone and install the project using the abovementioned installation instructions, opening up the pull request once you are finished.

## Credits: 

This project was developed by **Yaroslav Morozevych** and **Volodymyr Savchuk**, UCU, 2020

## License:  

Distributed under the MIT license. See ``LICENSE`` for more information.

