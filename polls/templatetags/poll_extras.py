from django import template
from jalali_date import date2jalali

register = template.Library()


@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')


@register.filter(name='show_jalali_date')
def show_jalali_date(value):
    return date2jalali(value)


@register.filter(name='three_digits_currency')
def three_digits_currency(value):
    try:
        # سعی می‌کنیم مقدار داده شده را به عدد اعشاری تبدیل کنیم
        numeric_value = float(value)
        # عدد را با جداکننده هزار فرمت می‌کنیم
        return '{:,.0f}'.format(numeric_value) + ' تومان'
    except (ValueError, TypeError):
        # اگر تبدیل موفقیت‌آمیز نبود، مقدار اصلی یا یک متن پیش‌فرض را برگردانیم
        # به صورت اختیاری می‌توانید خطا را لاگ کنید
        # import logging
        # logging.warning(f"Could not format value '{value}' as currency")
        return f"{value} تومان" # یا "" یا "مقدار نامعتبر" برگردانید

# @register.filter(name='three_digits_currency')
# def three_digits_currency(value: int):
#     return '{:,}'.format(value) + ' تومان'


@register.simple_tag
def multiply(quantity, price, *args, **kwargs):
    return three_digits_currency(quantity * price)
