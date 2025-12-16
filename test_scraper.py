import requests
from bs4 import BeautifulSoup

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
        print("در حال دریافت داده‌ها از سایت ماتیسا...")
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # پیدا کردن تمام ردیف‌های حاوی داده‌ها
            rows = soup.find_all('div', class_='row')
            
            print("\n" + "="*50)
            print("داده‌های استخراج شده از سایت ماتیسا:")
            print("="*50 + "\n")
            
            # شمارنده برای دسته‌بندی داده‌ها
            gold_items = []
            coin_items = []
            currency_items = []
            
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
                    # گرفتن قیمت واقعی از data-price اگر وجود داشته باشد
                    real_price = bottom_div.get('data-price', '').strip()
                    
                    # دسته‌بندی بر اساس نام کالا
                    if "طلا" in item_name or "مظنه" in item_name or "خرید" in item_name or "تعویض" in item_name:
                        gold_items.append((item_name, item_price, real_price))
                    elif "سکه" in item_name:
                        coin_items.append((item_name, item_price, real_price))
                    elif "دلار" in item_name or "یورو" in item_name or "درهم" in item_name:
                        currency_items.append((item_name, item_price, real_price))
            
            # نمایش داده‌های دسته‌بندی شده
            print("📊 قیمت‌های طلا:")
            print("-" * 40)
            for name, price, real_price in gold_items:
                print(f"• {name}: {price} تومان")
                if real_price:
                    print(f"  (قیمت واقعی: {real_price})")
            
            print("\n💰 قیمت‌های سکه:")
            print("-" * 40)
            for name, price, real_price in coin_items:
                print(f"• {name}: {price} تومان")
                if real_price:
                    print(f"  (قیمت واقعی: {real_price})")
            
            print("\n💱 نرخ ارزها:")
            print("-" * 40)
            for name, price, real_price in currency_items:
                print(f"• {name}: {price} تومان")
                if real_price:
                    print(f"  (قیمت واقعی: {real_price})")
            
            # نمایش زمان به‌روزرسانی
            update_time = soup.find(text=lambda text: text and 'بروزرسانی' in text)
            if update_time:
                print(f"\n🕒 آخرین به‌روزرسانی: {update_time.strip()}")
            else:
                print("\n🕒 زمان به‌روزرسانی یافت نشد")
            
            print("\n" + "="*50)
            print(f"✅ مجموعاً {len(gold_items) + len(coin_items) + len(currency_items)} مورد پیدا شد")
            print("="*50)
            
            return {
                'gold_prices': gold_items,
                'coin_prices': coin_items,
                'currency_rates': currency_items,
                'last_updated': update_time.strip() if update_time else None
            }
        else:
            print(f"❌ خطا در دریافت داده‌ها. کد وضعیت: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {str(e)}")
        return None

if __name__ == "__main__":
    print("🚀 شروع اسکرپینگ داده‌های قیمت طلا...")
    data = scrape_matisa_gold_prices()
    
    if data:
        print("\n✅ اسکرپینگ با موفقیت انجام شد!")
    else:
        print("\n❌ اسکرپینگ با شکست مواجه شد.")