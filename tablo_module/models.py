from django.db import models
from django.utils import timezone

class GoldPriceHistory(models.Model):
    """
    مدل برای ذخیره تاریخچه قیمت‌های طلا
    """
    date = models.DateTimeField(default=timezone.now, verbose_name="تاریخ")
    gold_18_carat = models.BigIntegerField(null=True, blank=True, verbose_name="طلا 18 عیار")
    gold_20_carat = models.BigIntegerField(null=True, blank=True, verbose_name="طلا 20 عیار")
    gold_21_carat = models.BigIntegerField(null=True, blank=True, verbose_name="طلا 21 عیار")
    gold_18_carat_retail = models.BigIntegerField(null=True, blank=True, verbose_name="خرید متفرقه طلا 18 عیار")
    gold_18_carat_exchange = models.BigIntegerField(null=True, blank=True, verbose_name="تعویض متفرقه طلا 18 عیار")
    gold_nugget = models.BigIntegerField(null=True, blank=True, verbose_name="مظنه نقدی")
    
    coin_emami = models.BigIntegerField(null=True, blank=True, verbose_name="سکه امامی")
    coin_tamam = models.BigIntegerField(null=True, blank=True, verbose_name="سکه تمام")
    coin_nim = models.BigIntegerField(null=True, blank=True, verbose_name="سکه نیم")
    coin_roob = models.BigIntegerField(null=True, blank=True, verbose_name="سکه ربع")
    coin_gerami = models.BigIntegerField(null=True, blank=True, verbose_name="سکه گرمی")
    
    currency_usd = models.BigIntegerField(null=True, blank=True, verbose_name="دلار")
    currency_eur = models.BigIntegerField(null=True, blank=True, verbose_name="یورو")
    currency_aed = models.BigIntegerField(null=True, blank=True, verbose_name="درهم")
    
    source_url = models.URLField(default="https://matisagoldgallery.com/tablo", verbose_name="منبع")
    
    class Meta:
        verbose_name = "تاریخچه قیمت طلا"
        verbose_name_plural = "تاریخچه قیمت‌های طلا"
        ordering = ['-date']
    
    def __str__(self):
        return f"قیمت‌های طلا - {self.date.strftime('%Y/%m/%d %H:%M')}"

class TabloSettings(models.Model):
    """
    تنظیمات ماژول تابلو
    """
    auto_update = models.BooleanField(default=True, verbose_name="به‌روزرسانی خودکار")
    update_interval_minutes = models.IntegerField(default=5, verbose_name="فاصله به‌روزرسانی (دقیقه)")
    last_update = models.DateTimeField(null=True, blank=True, verbose_name="آخرین به‌روزرسانی")
    api_enabled = models.BooleanField(default=True, verbose_name="فعال بودن API")
    
    class Meta:
        verbose_name = "تنظیمات تابلو"
        verbose_name_plural = "تنظیمات تابلو"
    
    def __str__(self):
        return "تنظیمات ماژول تابلو قیمت"