from django.urls import path
from . import views

# نام فضای نام (namespace) برای ماژول
app_name = 'gold_calculator'

# آدرس‌های ماژول
urlpatterns = [
    path('', views.gold_calculator_view, name='calculator_page'),
]