from django.db import models
from django.urls import reverse
from account_module.models import User


# Create your models here.

class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def __str__(self):
        return f'( {self.title} - {self.url_title} )'

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام برند', db_index=True)
    url_title = models.CharField(max_length=300, verbose_name='نام در url', db_index=True)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.title

class Product(models.Model):

    title = models.CharField(max_length=300, verbose_name='نام محصول')
    category = models.ManyToManyField(ProductCategory, related_name='product_categories', verbose_name='دسته بندی ها')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند', null=True, blank=True)
    # --- حذف فیلد: price = models.IntegerField(verbose_name='قیمت') ---
    short_description = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(verbose_name='توضیحات اصلی', db_index=True)
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    # +++ فیلدهای جدید برای محاسبه پویا +++
    product_code = models.CharField(max_length=100, unique=True, verbose_name='کد محصول', null=True, blank=True)
    weight_gram = models.FloatField(default=1.0, verbose_name='وزن (گرم)')
    GOLD_PURITY_CHOICES = [
        (18, '۱۸ عیار'),
        (21, '۲۱ عیار'),
        (24, '۲۴ عیار'),
    ]
    purity = models.IntegerField(choices=GOLD_PURITY_CHOICES, default=18, verbose_name='عیار طلا')
    making_charge_percent = models.FloatField(default=15.0, verbose_name='درصد اجرت ساخت')
    profit_percent = models.FloatField(default=7.0, verbose_name='درصد سود فروشگاه')
    is_available = models.BooleanField(default=True, verbose_name='موجود در انبار')
    
    # --- متدهای قبلی ---
    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])
    
    def __str__(self):
        return f"{self.title} ({self.weight_gram} گرم)"

    # +++ متد جدید: قلب تپنده محاسبات +++
    def calculate_final_price(self, gold_base_price_per_gram):
        """
        محاسبه قیمت نهایی محصول بر اساس قیمت پایه طلا.
        :param gold_base_price_per_gram: قیمت هر گرم طلای ۱۸ عیار خام
        :return: دیکشنری شامل تمام اجزای قیمت
        """
        # ۱. تطبیق قیمت پایه با عیار محصول (فرمول ساده)
        purity_factor = self.purity / 18.0
        adjusted_gold_price = gold_base_price_per_gram * purity_factor
        
        # ۲. قیمت طلای خام این محصول
        raw_gold_price = self.weight_gram * adjusted_gold_price
        
        # ۳. محاسبه اجرت و سود (مانند ماشین حساب)
        making_charge_amount = raw_gold_price * (self.making_charge_percent / 100.0)
        profit_amount = (raw_gold_price + making_charge_amount) * (self.profit_percent / 100.0)
        
        # ۴. محاسبه مالیات (۹٪ روی اجرت و سود)
        tax_amount = (making_charge_amount + profit_amount) * 0.09
        
        # ۵. قیمت نهایی
        final_price = raw_gold_price + making_charge_amount + profit_amount + tax_amount
        
        return {
            'final_price': int(final_price),  # قیمت نهایی به تومان
            'raw_gold_price': int(raw_gold_price),
            'making_charge_amount': int(making_charge_amount),
            'profit_amount': int(profit_amount),
            'tax_amount': int(tax_amount),
            'adjusted_gold_price_per_gram': int(adjusted_gold_price)  # قیمت هر گرم با عیار محصول
        } 
    
    @property
    def price(self):
        """
        فیلد مجازی برای سازگاری با کدهای قدیمی
        این متد به صورت خودکار قیمت فعلی محصول را برمی‌گرداند
        """
        try:
            from tablo_module.utils import get_gold_prices
            gold_data = get_gold_prices()
            gold_18k_price_str = gold_data.get('gold_prices', {}).get('طلا 18 عیار', '0')
            gold_base_price = int(''.join(filter(str.isdigit, str(gold_18k_price_str))))
            price_details = self.calculate_final_price(gold_base_price)
            return price_details['final_price']
        except:
            # مقدار پیش‌فرض ایمن در صورت خطا
            return 0




class ProductVisit(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='کاربر', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'
