/**
 * ماشین حساب قیمت طلا - منطق محاسبات لحظه‌ای
 */

// فرمت‌دهی اعداد با جداکننده هزارگان
function formatNumber(num) {
    return new Intl.NumberFormat('fa-IR').format(Math.round(num));
}

// محاسبه کامل قیمت طلا
function calculateGoldPrice() {
    // دریافت مقادیر از فرم
    const goldPrice = parseFloat(document.getElementById('gold-price').value) || 0;
    const weight = parseFloat(document.getElementById('weight').value) || 0;
    const makingChargePercent = parseFloat(document.getElementById('making-charge').value) || 0;
    const profitPercent = parseFloat(document.getElementById('profit').value) || 0;
    
    // 1. محاسبه قیمت طلای خام
    const rawGoldPrice = weight * goldPrice;
    
    // 2. محاسبه اجرت ساخت
    const makingCharge = rawGoldPrice * (makingChargePercent / 100);
    
    // 3. محاسبه سود فروشنده
    const profit = (rawGoldPrice + makingCharge) * (profitPercent / 100);
    
    // 4. محاسبه مالیات ارزش افزوده (۹٪ روی اجرت و سود)
    const tax = (makingCharge + profit) * 0.09;
    
    // 5. محاسبه قیمت نهایی
    const finalPrice = rawGoldPrice + makingCharge + profit + tax;
    
    // نمایش نتایج در صفحه
    document.getElementById('raw-gold-price').textContent = formatNumber(rawGoldPrice) + ' تومان';
    document.getElementById('making-charge-amount').textContent = formatNumber(makingCharge) + ' تومان';
    document.getElementById('profit-amount').textContent = formatNumber(profit) + ' تومان';
    document.getElementById('tax-amount').textContent = formatNumber(tax) + ' تومان';
    document.getElementById('final-price').textContent = formatNumber(finalPrice) + ' تومان';
}

// رویداد تغییر برای همه فیلدهای ورودی
function setupEventListeners() {
    const inputs = [
        'gold-price',
        'weight', 
        'making-charge',
        'profit'
    ];
    
    inputs.forEach(inputId => {
        const input = document.getElementById(inputId);
        if (input) {
            // محاسبه با تغییر مقدار
            input.addEventListener('input', calculateGoldPrice);
            
            // محاسبه با فشردن کلید
            input.addEventListener('keyup', calculateGoldPrice);
            
            // محاسبه با کلیک خارج از فیلد
            input.addEventListener('change', calculateGoldPrice);
        }
    });
}

// تابع کمکی برای اعتبارسنجی ورودی‌ها
function validateInputs() {
    const weight = document.getElementById('weight').value;
    const makingCharge = document.getElementById('making-charge').value;
    const profit = document.getElementById('profit').value;
    
    // اعتبارسنجی وزن
    if (weight <= 0) {
        alert('لطفاً وزن معتبری وارد کنید (بیشتر از صفر)');
        document.getElementById('weight').value = 1;
        return false;
    }
    
    // اعتبارسنجی درصدها
    if (makingCharge < 0 || makingCharge > 100) {
        alert('درصد اجرت ساخت باید بین ۰ تا ۱۰۰ باشد');
        document.getElementById('making-charge').value = 15;
        return false;
    }
    
    if (profit < 0 || profit > 100) {
        alert('درصد سود فروشنده باید بین ۰ تا ۱۰۰ باشد');
        document.getElementById('profit').value = 7;
        return false;
    }
    
    return true;
}

// تابع اصلی که هنگام بارگذاری صفحه اجرا می‌شود
document.addEventListener('DOMContentLoaded', function() {
    console.log('ماشین حساب طلا بارگذاری شد');
    
    // تنظیم رویدادها
    setupEventListeners();
    
    // اجرای محاسبه اولیه
    calculateGoldPrice();
    
    // اعتبارسنجی اولیه
    validateInputs();
    
    // افکت نمایش تدریجی
    const calculator = document.querySelector('.calculator-container');
    if (calculator) {
        calculator.style.opacity = '0';
        calculator.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            calculator.style.transition = 'all 0.5s ease';
            calculator.style.opacity = '1';
            calculator.style.transform = 'translateY(0)';
        }, 100);
    }
});

// تابع برای ریست کردن فرم
function resetCalculator() {
    document.getElementById('gold-price').value = '{{ default_gold_price }}';
    document.getElementById('weight').value = 5;
    document.getElementById('making-charge').value = 15;
    document.getElementById('profit').value = 7;
    
    calculateGoldPrice();
}