from django.shortcuts import render, HttpResponse
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from .modules.gmail_manager import GUser
import re


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
        return render(request, 'manage_page/chart.html', {"senders": ["Matthew Kenenitz", 'Vova Savchuk']})


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
        user = GUser()

        labels = user.defined_categories_info_dict.keys()
        default_items = user.defined_categories_info_dict.values()
        colors = ['#6F6CB1', '#F7C362', '#86CEC1', '#28C9D1']
        data = {
                "labels": labels,
                "default": default_items,
                "colors": colors
        }

        unread_info = user.unread_info_dict

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
        labels = ["Users", "Blue", "Yellow"]
        default_items = [4, 2, 2]
        colors = ['#6F6CB1', '#F7C362', '#86CEC1']
        data = {
            "labels": labels,
            "default": default_items,
            "colors": colors
        }
        return Response(data)


def get_sender(request):
    str_request = (str(request))

    pattern = re.compile(r"(?<=<WSGIRequest: GET '\/delete\/\?)(.*)(?=\=)")
    match = pattern.search(str_request)
    if match:
        sender = str.replace(str(match.group(0)), '+', ' ')
    print(sender)
    action = request.GET[sender]
    print(action)
    return HttpResponse('')
