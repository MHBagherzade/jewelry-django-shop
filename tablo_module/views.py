from django.views import View
from django.shortcuts import render
from django.utils import timezone
from .utils import get_gold_prices, format_price
from .models import TabloSettings

class TabloPageView(View):
    template_name = 'tablo_module/tablo_page.html'
    
    def get(self, request):
        # دریافت تنظیمات
        settings, created = TabloSettings.objects.get_or_create(id=1)
        
        # دریافت داده‌های قیمت طلا
        prices_data = get_gold_prices()
        
        # فرمت‌دهی داده‌ها برای نمایش
        formatted_data = {
            'last_updated': prices_data.get('last_updated', timezone.now().strftime("%H:%M")),
            'gold_prices': {},
            'coin_prices': {},
            'currency_rates': {}
        }
        
        # فرمت‌دهی قیمت‌های طلا
        for title, price in prices_data.get('gold_prices', {}).items():
            formatted_data['gold_prices'][title] = format_price(price)
        
        # فرمت‌دهی قیمت‌های سکه
        for title, price in prices_data.get('coin_prices', {}).items():
            formatted_data['coin_prices'][title] = format_price(price)
        
        # فرمت‌دهی نرخ ارزها
        for title, price in prices_data.get('currency_rates', {}).items():
            formatted_data['currency_rates'][title] = format_price(price)
        
        context = {
            'formatted_data': formatted_data,
            'settings': settings,
            'current_time': timezone.now().strftime("%Y/%m/%d %H:%M"),
            'site_setting': {'site_name': 'فروشگاه جواهرات'}  # برای عنوان صفحه
        }
        
        return render(request, self.template_name, context)
# from django.shortcuts import render
# from django.views import View
# from django.utils import timezone
# from django.core.cache import cache
# from django.http import JsonResponse
# from .utils import get_gold_prices, format_price
# from .models import GoldPriceHistory, TabloSettings

# class TabloPageView(View):
#     """
#     نمایش صفحه تابلو قیمت طلا
#     """
#     template_name = 'tablo_module/tablo_page.html'
    
#     def get(self, request):
#         # دریافت تنظیمات
#         settings, created = TabloSettings.objects.get_or_create(id=1)
        
#         # دریافت داده‌های فعلی
#         prices_data = get_gold_prices()
        
#         # اگر داده‌ای وجود ندارد، داده‌های پیش‌فرض برگردان
#         if not prices_data:
#             prices_data = {
#                 'last_updated': timezone.now().strftime("%H:%M"),
#                 'gold_prices': {},
#                 'coin_prices': {},
#                 'currency_rates': {}
#             }
        
#         # ذخیره در تاریخچه (هر 5 دقیقه یک بار)
#         should_save_history = False
#         last_history = GoldPriceHistory.objects.order_by('-date').first()
        
#         if not last_history:
#             should_save_history = True
#         else:
#             time_diff = (timezone.now() - last_history.date).total_seconds() / 60
#             if time_diff >= 5:
#                 should_save_history = True
        
#         if should_save_history and prices_data:
#             try:
#                 history = GoldPriceHistory()
                
#                 # ذخیره قیمت‌های طلا
#                 if 'gold_prices' in prices_data:
#                     gold_prices = prices_data['gold_prices']
#                     history.gold_18_carat = int(gold_prices.get('طلا_18_عیار', '0').replace(',', '')) if gold_prices.get('طلا_18_عیار') else None
#                     history.gold_20_carat = int(gold_prices.get('طلا_20_عیار', '0').replace(',', '')) if gold_prices.get('طلا_20_عیار') else None
#                     history.gold_21_carat = int(gold_prices.get('طلا_21_عیار', '0').replace(',', '')) if gold_prices.get('طلا_21_عیار') else None
#                     history.gold_18_carat_retail = int(gold_prices.get('خرید_متفرقه_طلا_18_عیار', '0').replace(',', '')) if gold_prices.get('خرید_متفرقه_طلا_18_عیار') else None
#                     history.gold_18_carat_exchange = int(gold_prices.get('تعویض_متفرقه_طلا18عیار', '0').replace(',', '')) if gold_prices.get('تعویض_متفرقه_طلا18عیار') else None
#                     history.gold_nugget = int(gold_prices.get('مظنه_نقدی', '0').replace(',', '')) if gold_prices.get('مظنه_نقدی') else None
                
#                 # ذخیره قیمت‌های سکه
#                 if 'coin_prices' in prices_data:
#                     coin_prices = prices_data['coin_prices']
#                     history.coin_emami = int(coin_prices.get('سکه_امامی', '0').replace(',', '')) if coin_prices.get('سکه_امامی') else None
#                     history.coin_tamam = int(coin_prices.get('سکه_تمام', '0').replace(',', '')) if coin_prices.get('سکه_تمام') else None
#                     history.coin_nim = int(coin_prices.get('سکه_نیم', '0').replace(',', '')) if coin_prices.get('سکه_نیم') else None
#                     history.coin_roob = int(coin_prices.get('سکه_ربع', '0').replace(',', '')) if coin_prices.get('سکه_ربع') else None
#                     history.coin_gerami = int(coin_prices.get('سکه_گرمی', '0').replace(',', '')) if coin_prices.get('سکه_گرمی') else None
                
#                 # ذخیره نرخ ارزها
#                 if 'currency_rates' in prices_data:
#                     currency_rates = prices_data['currency_rates']
#                     history.currency_usd = int(currency_rates.get('دلار', '0').replace(',', '')) if currency_rates.get('دلار') else None
#                     history.currency_eur = int(currency_rates.get('یورو', '0').replace(',', '')) if currency_rates.get('یورو') else None
#                     history.currency_aed = int(currency_rates.get('درهم', '0').replace(',', '')) if currency_rates.get('درهم') else None
                
#                 history.save()
                
#                 # به‌روزرسانی آخرین به‌روزرسانی در تنظیمات
#                 settings.last_update = timezone.now()
#                 settings.save()
                
#             except Exception as e:
#                 print(f"Error saving history: {str(e)}")
        
#         # تابع برای فرمت‌دهی نام‌ها
#         def format_title(key, category=''):
#             # جدا کردن کلمات با _
#             parts = key.replace('_', ' ').split()
            
#             # حذف کلمات تکراری
#             if category == 'gold' and 'طلا' in parts:
#                 parts = [p for p in parts if p != 'طلا']
#                 title = ' '.join(parts) + ' طلا'
#             elif category == 'coin' and 'سکه' in parts:
#                 parts = [p for p in parts if p != 'سکه']
#                 title = ' '.join(parts) + ' سکه'
#             elif category == 'currency' and 'ارز' in parts:
#                 parts = [p for p in parts if p != 'ارز']
#                 title = ' '.join(parts)
#             else:
#                 title = ' '.join(parts)
            
#             # حروف اول را بزرگ کن
#             title = title.title()
            
#             # جایگزینی کلمات خاص
#             replacements = {
#                 '18': '۱۸',
#                 '20': '۲۰',
#                 '21': '۲۱',
#                 'Emami': 'امامی',
#                 'Tamam': 'تمام',
#                 'Nim': 'نیم',
#                 'Roob': 'ربع',
#                 'Gerami': 'گرمی',
#                 'Dollar': 'دلار',
#                 'Euro': 'یورو',
#                 'Aed': 'درهم',
#                 'Retail': 'خرید متفرقه',
#                 'Exchange': 'تعویض متفرقه',
#                 'Nugget': 'مظنه نقدی',
#                 'عیار': 'عیار',
#                 'خرید': 'خرید',
#                 'متفرقه': 'متفرقه',
#                 'تعویض': 'تعویض',
#                 'مظنه': 'مظنه',
#                 'نقدی': 'نقدی'
#             }
            
#             for en, fa in replacements.items():
#                 title = title.replace(en, fa)
            
#             return title
        
#         # فرمت‌دهی داده‌ها
#         formatted_gold_prices = {}
#         for key, value in prices_data.get('gold_prices', {}).items():
#             title = format_title(key, 'gold')
#             formatted_gold_prices[title] = format_price(value)
        
#         formatted_coin_prices = {}
#         for key, value in prices_data.get('coin_prices', {}).items():
#             title = format_title(key, 'coin')
#             formatted_coin_prices[title] = format_price(value)
        
#         formatted_currency_rates = {}
#         for key, value in prices_data.get('currency_rates', {}).items():
#             title = format_title(key, 'currency')
#             formatted_currency_rates[title] = format_price(value)
        
#         # آماده‌سازی داده‌ها برای نمایش
#         context = {
#             'prices_data': prices_data,
#             'formatted_data': {
#                 'last_updated': prices_data.get('last_updated', timezone.now().strftime("%H:%M")),
#                 'gold_prices': formatted_gold_prices,
#                 'coin_prices': formatted_coin_prices,
#                 'currency_rates': formatted_currency_rates,
#             },
#             'settings': settings,
#             'current_time': timezone.now().strftime("%Y/%m/%d %H:%M"),
#         }
        
#         return render(request, self.template_name, context)

# class TabloDataAPIView(View):
#     """
#     API برای دریافت داده‌های تابلو در قالب JSON
#     """
#     def get(self, request):
#         prices_data = get_gold_prices()
#         return JsonResponse({
#             'data': prices_data,
#             'timestamp': timezone.now().isoformat(),
#             'success': True
#         })