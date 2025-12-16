# from django.urls import path
# from . import views

# app_name = 'tablo_module'

# urlpatterns = [
#     path('', views.TabloPageView.as_view(), name='tablo_page'),
#     path('api/tablo-data/', views.TabloDataAPIView.as_view(), name='tablo_data_api'),
# ]
from django.urls import path
from . import views

app_name = 'tablo_module'

urlpatterns = [
    path('', views.TabloPageView.as_view(), name='tablo_page'),
]