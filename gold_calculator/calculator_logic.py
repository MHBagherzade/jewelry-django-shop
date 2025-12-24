def calculate_gold_price(weight, gold_price, making_charge_percent, profit_percent):
    """
    محاسبه کامل قیمت طلا بر اساس فرمول اتحادیه طلا
    
    پارامترها:
    - weight: وزن طلا بر حسب گرم
    - gold_price: قیمت هر گرم طلای خام
    - making_charge_percent: درصد اجرت ساخت
    - profit_percent: درصد سود فروشنده
    
    بازگشت:
    - دیکشنری شامل تمام محاسبات
    """
    # 1. قیمت طلای خام
    raw_gold_price = weight * gold_price
    
    # 2. اجرت ساخت
    making_charge = raw_gold_price * (making_charge_percent / 100)
    
    # 3. سود فروشنده
    profit = (raw_gold_price + making_charge) * (profit_percent / 100)
    
    # 4. مالیات ارزش افزوده (۹٪ فقط روی اجرت و سود)
    tax = (making_charge + profit) * 0.09
    
    # 5. قیمت نهایی
    final_price = raw_gold_price + making_charge + profit + tax
    
    return {
        'raw_gold_price': raw_gold_price,
        'making_charge': making_charge,
        'profit': profit,
        'tax': tax,
        'final_price': final_price
    }


def format_price(price):
    """
    فرمت‌دهی قیمت به صورت زیبا با جداکننده هزارگان
    """
    try:
        return f"{int(price):,}"
    except:
        return str(price)