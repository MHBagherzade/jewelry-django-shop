from django.contrib import admin
from django.utils.html import format_html
from . import models
from tablo_module.utils import get_gold_prices
from django.utils import timezone

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_filter = ['category', 'is_active', 'brand']
    list_display = ['title', 'display_price', 'brand', 'weight_gram', 'purity', 'is_active', 'is_delete']
    list_editable = ['is_active']
    readonly_fields = ['product_code', 'display_price_details']
    search_fields = ['title', 'product_code']
    filter_horizontal = ['category']  # برای نمایش بهتر دسته‌بندی‌های چندگانه
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'brand', 'category', 'image', 'product_code')
        }),
        ('مشخصات فنی', {
            'fields': ('weight_gram', 'purity', 'making_charge_percent', 'profit_percent')
        }),
        ('توضیحات', {
            'fields': ('short_description', 'description', 'slug')
        }),
        ('وضعیت', {
            'fields': ('is_active', 'is_delete', 'is_available')
        }),
        ('قیمت‌گذاری پویا', {
            'fields': ('display_price_details',),
            'description': 'قیمت محصول به صورت خودکار بر اساس تابلو قیمت طلا محاسبه می‌شود'
        }),
    )
    
    def display_price(self, obj):
        """
        نمایش قیمت پویا در لیست ادمین
        """
        try:
            # دریافت آخرین قیمت طلا از کش
            prices_data = get_gold_prices()
            gold_prices = prices_data.get('gold_prices', {})
            
            # دریافت قیمت طلا 18 عیار
            gold_18_price_str = gold_prices.get('طلا 18 عیار', '0')
            
            # استخراج عدد از قیمت
            gold_18_price = int(''.join(filter(str.isdigit, gold_18_price_str)))
            
            # محاسبه قیمت نهایی
            price_details = obj.calculate_final_price(gold_18_price)
            
            # نمایش با فرمت مناسب
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">{} تومان</span><br>'
                '<small style="color: #6c757d;">آخرین به‌روزرسانی: {}</small>',
                f"{price_details['final_price']:,}",
                timezone.now().strftime("%H:%M")
            )
        except Exception as e:
            return format_html(
                '<span style="color: #dc3545;">خطا در محاسبه: {}</span>',
                str(e)
            )
    
    display_price.short_description = 'قیمت'
    display_price.admin_order_field = 'title'
    
    def display_price_details(self, obj):
        """
        نمایش جزئیات قیمت در فرم ویرایش
        """
        try:
            prices_data = get_gold_prices()
            gold_prices = prices_data.get('gold_prices', {})
            gold_18_price_str = gold_prices.get('طلا 18 عیار', '0')
            gold_18_price = int(''.join(filter(str.isdigit, gold_18_price_str)))
            
            price_details = obj.calculate_final_price(gold_18_price)
            
            html = f"""
            <div style="border: 1px solid #dee2e6; border-radius: 5px; padding: 15px; background: #f8f9fa;">
                <h4 style="color: #007bff; margin-bottom: 15px;">جزئیات محاسبه قیمت</h4>
                <table style="width: 100%;">
                    <tr>
                        <td style="padding: 5px 0; width: 30%;"><strong>قیمت پایه طلا 18 عیار:</strong></td>
                        <td style="padding: 5px 0; text-align: left;">{gold_18_price:,} تومان</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px 0;"><strong>وزن محصول:</strong></td>
                        <td style="padding: 5px 0; text-align: left;">{obj.weight_gram} گرم</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px 0;"><strong>عیار طلا:</strong></td>
                        <td style="padding: 5px 0; text-align: left;">{obj.get_purity_display()}</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px 0;"><strong>قیمت طلای خام:</strong></td>
                        <td style="padding: 5px 0; text-align: left; color: #198754;">{price_details['raw_gold_price']:,} تومان</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px 0;"><strong>اجر ساخت ({obj.making_charge_percent}%):</strong></td>
                        <td style="padding: 5px 0; text-align: left; color: #0d6efd;">{price_details['making_charge_amount']:,} تومان</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px 0;"><strong>سود فروشگاه ({obj.profit_percent}%):</strong></td>
                        <td style="padding: 5px 0; text-align: left; color: #ffc107;">{price_details['profit_amount']:,} تومان</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px 0;"><strong>مالیات (9%):</strong></td>
                        <td style="padding: 5px 0; text-align: left; color: #fd7e14;">{price_details['tax_amount']:,} تومان</td>
                    </tr>
                    <tr style="border-top: 1px solid #dee2e6; margin-top: 10px;">
                        <td style="padding: 10px 0; font-weight: bold;"><strong>قیمت نهایی:</strong></td>
                        <td style="padding: 10px 0; text-align: left; font-weight: bold; color: #dc3545;">{price_details['final_price']:,} تومان</td>
                    </tr>
                </table>
                <p style="margin-top: 10px; color: #6c757d; font-size: 0.85em;">
                    <i class="fa fa-info-circle"></i> قیمت‌ها به صورت لحظه‌ای و بر اساس تابلو قیمت محاسبه می‌شوند
                </p>
            </div>
            """
            return format_html(html)
        except Exception as e:
            return format_html(
                '<div style="color: #dc3545; padding: 10px; background: #f8d7da; border-radius: 4px;">'
                '<strong>خطا در محاسبه قیمت:</strong> {}</div>',
                str(e)
            )
    
    display_price_details.short_description = 'جزئیات قیمت'
    display_price_details.allow_tags = True

# ثبت مدل‌ها در ادمین
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductVisit)
admin.site.register(models.ProductGallery)