from django.core.management.base import BaseCommand
from tablo_module.utils import scrape_gold_prices
from tablo_module.models import GoldPriceHistory, TabloSettings
from django.utils import timezone

class Command(BaseCommand):
    help = 'به‌روزرسانی خودکار قیمت‌های طلا'

    def handle(self, *args, **options):
        self.stdout.write('در حال به‌روزرسانی قیمت‌های طلا...')
        
        # اسکرپ داده‌ها
        data = scrape_gold_prices()
        
        if data:
            # ذخیره در تاریخچه
            try:
                history = GoldPriceHistory()
                
                # ذخیره قیمت‌های طلا
                if 'gold_prices' in data:
                    gold_prices = data['gold_prices']
                    history.gold_18_carat = int(gold_prices.get('طلا_18_عیار', '0').replace(',', '')) if gold_prices.get('طلا_18_عیار') else None
                    history.gold_20_carat = int(gold_prices.get('طلا_20_عیار', '0').replace(',', '')) if gold_prices.get('طلا_20_عیار') else None
                    history.gold_21_carat = int(gold_prices.get('طلا_21_عیار', '0').replace(',', '')) if gold_prices.get('طلا_21_عیار') else None
                    history.gold_18_carat_retail = int(gold_prices.get('خرید_متفرقه_طلا_18_عیار', '0').replace(',', '')) if gold_prices.get('خرید_متفرقه_طلا_18_عیار') else None
                    history.gold_18_carat_exchange = int(gold_prices.get('تعویض_متفرقه_طلا18عیار', '0').replace(',', '')) if gold_prices.get('تعویض_متفرقه_طلا18عیار') else None
                    history.gold_nugget = int(gold_prices.get('مظنه_نقدی', '0').replace(',', '')) if gold_prices.get('مظنه_نقدی') else None
                
                # ذخیره قیمت‌های سکه
                if 'coin_prices' in data:
                    coin_prices = data['coin_prices']
                    history.coin_emami = int(coin_prices.get('سکه_امامی', '0').replace(',', '')) if coin_prices.get('سکه_امامی') else None
                    history.coin_tamam = int(coin_prices.get('سکه_تمام', '0').replace(',', '')) if coin_prices.get('سکه_تمام') else None
                    history.coin_nim = int(coin_prices.get('سکه_نیم', '0').replace(',', '')) if coin_prices.get('سکه_نیم') else None
                    history.coin_roob = int(coin_prices.get('سکه_ربع', '0').replace(',', '')) if coin_prices.get('سکه_ربع') else None
                    history.coin_gerami = int(coin_prices.get('سکه_گرمی', '0').replace(',', '')) if coin_prices.get('سکه_گرمی') else None
                
                # ذخیره نرخ ارزها
                if 'currency_rates' in data:
                    currency_rates = data['currency_rates']
                    history.currency_usd = int(currency_rates.get('دلار', '0').replace(',', '')) if currency_rates.get('دلار') else None
                    history.currency_eur = int(currency_rates.get('یورو', '0').replace(',', '')) if currency_rates.get('یورو') else None
                    history.currency_aed = int(currency_rates.get('درهم', '0').replace(',', '')) if currency_rates.get('درهم') else None
                
                history.save()
                
                # به‌روزرسانی تنظیمات
                settings, created = TabloSettings.objects.get_or_create(id=1)
                settings.last_update = timezone.now()
                settings.save()
                
                self.stdout.write(self.style.SUCCESS('قیمت‌های طلا با موفقیت به‌روزرسانی شدند'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'خطا در ذخیره تاریخچه: {str(e)}'))
        else:
            self.stdout.write(self.style.ERROR('خطا در اسکرپینگ داده‌ها'))
        
        # نباید مقداری برگرداند (None برگرداند)
        return None