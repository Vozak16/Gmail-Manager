from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from .modules import containers


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
        pass


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
        labels = ["Users", "Blue", "Yellow"]
        default_items = [4, 2, 2]
        colors = ['#6F6CB1', '#F7C362', '#86CEC1']
        data = {
                "labels": labels,
                "default": default_items,
                "colors": colors
        }

        labels_unread = ["Unread", "Read"]
        default_items_unread = [256, 87]
        colors_unread = ['#6F6CB1', '#CBC9E4']
        data_unread = {
            "labels": labels_unread,
            "default": default_items_unread,
            "colors": colors_unread
        }

        all_data = {
            "data": data,
            "data_unread": data_unread
        }
        return Response(all_data)
