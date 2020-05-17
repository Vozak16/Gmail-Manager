from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.GetStarted.as_view(), name='home'),
    url(r'^home$', views.HomeView.as_view(), name='home'),
    url(r'^api/chart/data/$', views.ChartData.as_view())
]
