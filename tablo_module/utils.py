import requests
from bs4 import BeautifulSoup
from django.core.cache import cache
from django.utils import timezone

def scrape_matisa_gold_prices():
    """
    اسکرپینگ داده‌های قیمت طلا از سایت ماتیسا
    """
    url = "https://matisagoldgallery.com/tablo"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # پیدا کردن تمام ردیف‌های حاوی داده‌ها
            rows = soup.find_all('div', class_='row')
            
            # شمارنده برای دسته‌بندی داده‌ها
            gold_items = {}
            coin_items = {}
            currency_items = {}
            
            # بررسی هر ردیف
            for row in rows:
                # پیدا کردن div با کلاس top shadow (نام کالا)
                top_div = row.find('div', class_='top shadow')
                # پیدا کردن div با کلاس bottom shadow (قیمت)
                bottom_div = row.find('div', class_='bottom shadow')
                
                if top_div and bottom_div:
                    # گرفتن متن نام کالا
                    item_name = top_div.text.strip()
                    # گرفتن متن قیمت (مقدار نمایش داده شده)
                    item_price = bottom_div.text.strip()
                    
                    # دسته‌بندی بر اساس نام کالا
                    if "طلا" in item_name or "مظنه" in item_name or "خرید" in item_name or "تعویض" in item_name:
                        gold_items[item_name] = item_price
                    elif "سکه" in item_name:
                        coin_items[item_name] = item_price
                    elif "دلار" in item_name or "یورو" in item_name or "درهم" in item_name:
                        currency_items[item_name] = item_price
            
            # نمایش زمان به‌روزرسانی
            update_time = soup.find(text=lambda text: text and 'بروزرسانی' in text)
            
            # ساخت دیکشنری نهایی
            data = {
                'last_updated': update_time.strip() if update_time else timezone.now().strftime("%H:%M"),
                'gold_prices': gold_items,
                'coin_prices': coin_items,
                'currency_rates': currency_items
            }
            
            # ذخیره در کش برای 5 دقیقه
            cache.set('gold_prices_data', data, timeout=300)
            return data
        else:
            # بازگشت داده‌های پیش‌فرض در صورت خطا
            return get_default_gold_prices()
            
    except Exception as e:
        print(f"Error scraping gold prices: {str(e)}")
        return get_default_gold_prices()

def get_default_gold_prices():
    """داده‌های پیش‌فرض در صورت خطا"""
    return {
        'last_updated': timezone.now().strftime("%H:%M"),
        'gold_prices': {
            'طلا 18 عیار': '12,500,000',
            'طلا 20 عیار': '13,900,000',
            'طلا 21 عیار': '14,600,000',
            'خرید متفرقه طلا 18 عیار': '12,300,000',
            'تعویض متفرقه طلا 18 عیار': '12,400,000',
            'مظنه نقدی': '54,400,000'
        },
        'coin_prices': {
            'سکه امامی': '130,000',
            'سکه تمام': '124,000',
            'سکه نیم': '69,000',
            'سکه ربع': '39,000',
            'سکه گرمی': '18,500'
        },
        'currency_rates': {
            'دلار': '122,000',
            'یورو': '143,000',
            'درهم': '33,800'
        }
    }

def get_gold_prices():
    """
    دریافت داده‌های قیمت طلا از کش یا اسکرپینگ مجدد
    """
    # اول چک کنیم که آیا داده در کش وجود دارد
    cached_data = cache.get('gold_prices_data')
    if cached_data:
        return cached_data
    
    # اگر کش وجود ندارد، داده‌ها را اسکرپ کن
    return scrape_matisa_gold_prices()

def format_price(price_str):
    """فرمت‌دهی قیمت به صورت خوانا"""
    try:
        if isinstance(price_str, str):
            # حذف کاراکترهای غیرعددی
            clean_price = ''.join(c for c in price_str if c.isdigit())
            if clean_price:
                price = int(clean_price)
                return f"{price:,}"
        return price_str
    except:
        return price_str
# import requests
# from bs4 import BeautifulSoup
# import json
# import time
# from django.core.cache import cache
# from django.utils import timezone

# # دیکشنری گلوبال برای ذخیره داده‌ها
# GOLD_PRICES_CACHE = {}

# def scrape_gold_prices():
#     """
#     اسکرپینگ داده‌های قیمت طلا از سایت ماتیسا
#     """
#     url = "https://matisagoldgallery.com/tablo"
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7',
#     }
    
#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         response.encoding = 'utf-8'
        
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             # استخراج داده‌ها بر اساس ساختار صفحه
#             data = {
#                 'last_updated': None,
#                 'gold_prices': {},
#                 'coin_prices': {},
#                 'currency_rates': {}
#             }
            
#             # پیدا کردن آخرین زمان به‌روزرسانی
#             update_time_element = soup.find(string=lambda text: text and 'بروزرسانی' in text)
#             if update_time_element:
#                 data['last_updated'] = update_time_element.strip().replace('بروزرسانی', '').strip()
#             else:
#                 data['last_updated'] = timezone.now().strftime("%H:%M")
            
#             # پیدا کردن قیمت‌های طلا
#             gold_section = soup.find(string=lambda text: text and 'قیمت لحظه ای طلا' in text)
#             if gold_section:
#                 parent_div = gold_section.find_parent('div')
#                 if parent_div:
#                     gold_table = parent_div.find_next('div')
#                     if gold_table:
#                         for row in gold_table.find_all('div', class_='row'):
#                             title_div = row.find('div', class_='title')
#                             price_div = row.find('div', class_='price')
#                             if title_div and price_div:
#                                 title = title_div.text.strip()
#                                 price = price_div.text.strip().replace(',', '')
#                                 key = title.replace(' ', '_').lower()
#                                 data['gold_prices'][key] = price
            
#             # پیدا کردن قیمت‌های سکه
#             coin_section = soup.find(string=lambda text: text and 'قیمت لحظه ای سکه' in text)
#             if coin_section:
#                 parent_div = coin_section.find_parent('div')
#                 if parent_div:
#                     coin_table = parent_div.find_next('div')
#                     if coin_table:
#                         for row in coin_table.find_all('div', class_='row'):
#                             title_div = row.find('div', class_='title')
#                             price_div = row.find('div', class_='price')
#                             if title_div and price_div:
#                                 title = title_div.text.strip()
#                                 price = price_div.text.strip().replace(',', '')
#                                 key = title.replace(' ', '_').lower()
#                                 data['coin_prices'][key] = price
            
#             # پیدا کردن نرخ ارزها
#             currency_section = soup.find(string=lambda text: text and 'قیمت لحظه ای ارز' in text)
#             if currency_section:
#                 parent_div = currency_section.find_parent('div')
#                 if parent_div:
#                     currency_table = parent_div.find_next('div')
#                     if currency_table:
#                         for row in currency_table.find_all('div', class_='row'):
#                             title_div = row.find('div', class_='title')
#                             price_div = row.find('div', class_='price')
#                             if title_div and price_div:
#                                 title = title_div.text.strip()
#                                 price = price_div.text.strip().replace(',', '')
#                                 key = title.replace(' ', '_').lower()
#                                 data['currency_rates'][key] = price
            
#             # ذخیره در کش و دیکشنری گلوبال
#             cache.set('gold_prices_data', data, timeout=300)  # 5 دقیقه کش
#             global GOLD_PRICES_CACHE
#             GOLD_PRICES_CACHE = data
            
#             return data
#         else:
#             print(f"Failed to fetch data. Status code: {response.status_code}")
#             return None
            
#     except Exception as e:
#         print(f"Error scraping gold prices: {str(e)}")
#         return None

# def get_gold_prices():
#     """
#     دریافت داده‌های قیمت طلا از کش یا اسکرپینگ مجدد
#     """
#     global GOLD_PRICES_CACHE
    
#     # اول چک کنیم که آیا داده در کش وجود دارد
#     cached_data = cache.get('gold_prices_data')
#     if cached_data:
#         GOLD_PRICES_CACHE = cached_data
#         return cached_data
    
#     # اگر کش وجود ندارد، داده‌ها را اسکرپ کن
#     return scrape_gold_prices()

# def format_price(price_str):
#     """
#     فرمت‌دهی قیمت به صورت خوانا
#     """
#     try:
#         if isinstance(price_str, str):
#             # حذف کاراکترهای غیرعددی
#             clean_price = ''.join(c for c in price_str if c.isdigit())
#             if clean_price:
#                 price = int(clean_price)
#                 return f"{price:,}"
#         return price_str
#     except (ValueError, TypeError):
#         return price_str

# # هنگام استارت اپلیکیشن، داده‌ها را بارگذاری کن
# def load_initial_data():
#     """بارگذاری اولیه داده‌ها"""
#     print("Loading initial gold prices data...")
#     data = get_gold_prices()
#     if data:
#         print("Initial gold prices data loaded successfully!")
#     else:
#         print("Failed to load initial gold prices data.")

