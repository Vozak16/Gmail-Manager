from django.shortcuts import render, HttpResponse
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from .modules.gmail_manager import GUser
import re

GMAIL_USER = None


class GetStarted(View):
    """
    Create a Get Started Page
    """
    @staticmethod
    def get(request):
        """
        Return a rendered template

        :param request: Django request
        :return: Django.render
        """
        global GMAIL_USER
        GMAIL_USER = GUser()
        return render(request, 'get_started/get_started.html')


class HomeView(View):
    """
    Create a Home page
    """
    @staticmethod
    def get(request):
        """
        Return a rendered template

        :param request: Django request
        :return: Django.render
        """
        return render(request, 'home_page/chart.html', {})


class ChartData(APIView):
    """
    Create a ChartData class with REST Framework
    """
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def get(request):
        """
        Return a JSON response

        :return: response
        """

        global GMAIL_USER
        labels = GMAIL_USER.defined_categories_info_dict.keys()
        default_items = GMAIL_USER.defined_categories_info_dict.values()
        colors = ['#6F6CB1', '#86CEC1', '#F7C362']
        data = {
                "labels": labels,
                "default": default_items,
                "colors": colors
        }

        unread_info = GMAIL_USER.unread_info_dict

        print(unread_info)
        data_unread = {
            "labels": unread_info.keys(),
            "default": unread_info.values(),
        }
        colors_unread = ['#6F6CB1', '#CBC9E4']
        data_unread['colors'] = colors_unread

        all_data = {
            "data": data,
            "data_unread": data_unread
        }
        return Response(all_data)


class ManageView(View):
    """
    Create a Home page
    """
    @staticmethod
    def get(request):
        """
        Return a rendered template

        :param request: Django request
        :return: Django.render
        """
        category = request.GET['btn']
        # цей найшвидший
        if category == 'Promotions':
            category = 'CATEGORY_PROMOTIONS'
        elif category == 'Social':
            category = 'CATEGORY_SOCIAL'
        elif category == 'Updates':
            category = 'CATEGORY_UPDATES'

        global GMAIL_USER
        GMAIL_USER.get_inbox_info(category)

        return render(request, 'manage_page/chart.html', {"senders": GMAIL_USER.lst_sender_sub})


class ManageChartData(APIView):
    """
    Create a ChartData class with REST Framework
    """
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def get(request):
        """
        Return a JSON response

        :return: response
        """
        global GMAIL_USER
        labels = GMAIL_USER.chart_inbox_info.keys()
        default_items = GMAIL_USER.chart_inbox_info.values()
        colors = ['#6F6CB1', '#CBC9E4', '#86CEC1', '#A6DAD2', '#6396B9', '#A0C8DF', '#F7C362', '#F2CC8f', '#E25470',
                  '#ED8CA4', '#6F6CB1', '#CBC9E4', '#86CEC1', '#6A6DAD2', '#6396B9', '#A0C8DF', '#F7C362', '#F2CC8f', '#E25470',
                  '#ED8CA4', '#6F6CB1', '#CBC9E4', '#86CEC1', '#6A6DAD2', '#6396B9', '#A0C8DF', '#F7C362', '#F2CC8f', '#E25470',
                  '#ED8CA4']
        colors = colors[:len(labels)]
        data = {
            "labels": labels,
            "default": default_items,
            "colors": colors
        }
        return Response(data)


class ModifyManageView(View):
    @staticmethod
    def get(request):
        global sender_dict
        str_request = (str(request))

        pattern = re.compile(r"(?<=<WSGIRequest: GET '\/delete\/\?)(.*)(?=\=)")
        match = pattern.search(str_request)
        if match:
            sender = str.replace(str(match.group(0)), '+', ' ')
        action = request.GET[sender]

        if action == 'Quick Trash':
            GMAIL_USER.delete_messages(sender)
            print(GMAIL_USER.chart_inbox_info)
            print(GMAIL_USER.lst_sender_sub)
        elif action == 'Unsubscribe':
            GMAIL_USER.unsubscribe(sender)

        return render(request, 'modify_manage_page/modify_manage_page.html', {"senders": GMAIL_USER.lst_sender_sub})


class ModifyChartData(APIView):
    @staticmethod
    def get(request):

        global GMAIL_USER
        print(GMAIL_USER.chart_inbox_info)
        labels = GMAIL_USER.chart_inbox_info.keys()
        default_items = GMAIL_USER.chart_inbox_info.values()
        colors = ['#6F6CB1', '#F7C362', '#86CEC1', '#6F6CB1', '#F7C362', '#86CEC1', '#6F6CB1', '#F7C362', '#86CEC1',
                  '#6F6CB1', '#F7C362', '#86CEC1', '#6F6CB1', '#F7C362', '#86CEC1', '#6F6CB1', '#F7C362', '#86CEC1',
                  '#6F6CB1', '#F7C362', '#86CEC1', '#6F6CB1', '#F7C362', '#86CEC1']
        colors = colors[:len(labels)]
        data = {
            "labels": labels,
            "default": default_items,
            "colors": colors
        }
        return Response(data)
