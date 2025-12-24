from django.shortcuts import render
from tablo_module.utils import get_gold_prices

def gold_calculator_view(request):
    """
    نمایش صفحه ماشین حساب طلا
    """
    # دریافت قیمت لحظه‌ای طلا از ماژول tablo
    gold_data = get_gold_prices()
    
    # استخراج قیمت طلای ۱۸ عیار
    default_gold_price = 12500000  # مقدار پیش‌فرض
    gold_18k = gold_data.get('gold_prices', {}).get('طلا 18 عیار', '0')
    
    # تمیز کردن قیمت (حذف کاما و کاراکترهای غیرعددی)
    try:
        clean_price = ''.join(c for c in str(gold_18k) if c.isdigit())
        if clean_price:
            default_gold_price = int(clean_price)
    except:
        pass  # در صورت خطا همان مقدار پیش‌فرض باقی می‌ماند
    
    # نمونه محاسبه برای نمایش اولیه در صفحه
    sample_weight = 5
    making_percent = 15
    profit_percent = 7
    
    raw_price = sample_weight * default_gold_price
    making_charge = raw_price * (making_percent / 100)
    profit = (raw_price + making_charge) * (profit_percent / 100)
    tax = (making_charge + profit) * 0.09
    final_price = raw_price + making_charge + profit + tax
    
    # داده‌های ارسال شده به تمپلیت
    context = {
        'default_gold_price': default_gold_price,
        'last_updated': gold_data.get('last_updated', ''),
        'sample_calculation': {
            'raw_price': raw_price,
            'making_charge': making_charge,
            'profit': profit,
            'tax': tax,
            'final_price': final_price
        },
        'site_setting': {'site_name': 'فروشگاه جواهرات'}
    }
    
    # رندر کردن صفحه از پوشه templates داخلی ماژول
    return render(request, 'gold_calculator/calculator.html', context)