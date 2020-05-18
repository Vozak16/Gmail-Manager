from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from .modules.gmail_manager import GUser


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
        user = GUser()
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
