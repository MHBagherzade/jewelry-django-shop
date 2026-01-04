from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from site_module.models import SiteBanner
from utils.http_service import get_client_ip
from utils.convertors import group_list
from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery
# +++ وارد کردن ماژول قیمت لحظه‌ای +++
from tablo_module.utils import get_gold_prices




class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 6  # حذف ordering چون قیمت پویاست

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # +++ استفاده از سیستم جدید برای ماکزیمم قیمت +++
        try:
            from tablo_module.utils import get_gold_prices
            gold_data = get_gold_prices()
            gold_18k_price_str = gold_data.get('gold_prices', {}).get('طلا 18 عیار', '0')
            gold_base_price = int(''.join(filter(str.isdigit, str(gold_18k_price_str))))
            
            # محاسبه ماکزیمم قیمت از تمام محصولات
            max_price = 0
            for product in Product.objects.filter(is_active=True, is_delete=False):
                price_details = product.calculate_final_price(gold_base_price)
                if price_details['final_price'] > max_price:
                    max_price = price_details['final_price']
        except:
            max_price = 100000000  # مقدار پیش‌فرض
        
        context['db_max_price'] = max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True, position__iexact=SiteBanner.SiteBannerPositions.product_list)
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True, is_delete=False)
        
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        
        # +++ اصلاح فیلترهای قیمت با استفاده از فیلد مجازی +++
        if start_price or end_price:
            try:
                from tablo_module.utils import get_gold_prices
                gold_data = get_gold_prices()
                gold_18k_price_str = gold_data.get('gold_prices', {}).get('طلا 18 عیار', '0')
                gold_base_price = int(''.join(filter(str.isdigit, str(gold_18k_price_str))))
                
                # فیلتر دستی بر اساس قیمت پویا
                filtered_products = []
                for product in queryset:
                    actual_price = product.price  # استفاده از فیلد مجازی
                    if start_price and actual_price < float(start_price):
                        continue
                    if end_price and actual_price > float(end_price):
                        continue
                    filtered_products.append(product)
                queryset = filtered_products
            except:
                pass  # در صورت خطا، همه محصولات نمایش داده شوند
        
        # +++ فیلترهای برند و دسته‌بندی +++
        if brand_name:
            queryset = [p for p in queryset if p.brand and p.brand.url_title.lower() == brand_name.lower()]
        
        if category_name:
            queryset = [p for p in queryset if any(cat.url_title.lower() == category_name.lower() for cat in p.category.all())]
        
        return queryset

# class ProductListView(ListView):
#     template_name = 'product_module/product_list.html'
#     model = Product
#     context_object_name = 'products'
#     ordering = ['-price']
#     paginate_by = 6

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(ProductListView, self).get_context_data()
#         query = Product.objects.all()
#         product: Product = query.order_by('-price').first()
#         db_max_price = product.price if product is not None else 0
#         context['db_max_price'] = db_max_price
#         context['start_price'] = self.request.GET.get('start_price') or 0
#         context['end_price'] = self.request.GET.get('end_price') or db_max_price
#         context['banners'] = SiteBanner.objects.filter(is_active=True, position__iexact=SiteBanner.SiteBannerPositions.product_list)
#         return context

#     def get_queryset(self):
#         query = super(ProductListView, self).get_queryset()
#         category_name = self.kwargs.get('cat')
#         brand_name = self.kwargs.get('brand')
#         request: HttpRequest = self.request
#         start_price = request.GET.get('start_price')
#         end_price = request.GET.get('end_price')
#         if start_price is not None:
#             query = query.filter(price__gte=start_price)

#         if end_price is not None:
#             query = query.filter(price__lte=end_price)

#         if brand_name is not None:
#             query = query.filter(brand__url_title__iexact=brand_name)

#         if category_name is not None:
#             query = query.filter(category__url_title__iexact=category_name)
#         return query


# class ProductDetailView(DetailView):
#     template_name = 'product_module/product_detail.html'
#     model = Product

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         loaded_product = self.object
#         request = self.request
#         favorite_product_id = request.session.get("product_favorites")
#         context['is_favorite'] = favorite_product_id == str(loaded_product.id)
#         context['banners'] = SiteBanner.objects.filter(is_active=True, position__iexact=SiteBanner.SiteBannerPositions.product_detail)
#         galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id).all())
#         galleries.insert(0, loaded_product)
#         context['product_galleries_group'] = group_list(galleries, 3)
#         context['related_products'] = group_list(list(Product.objects.filter(brand_id=loaded_product.brand_id).exclude(pk=loaded_product.id).all()[:12]), 3)
#         user_ip = get_client_ip(self.request)
#         user_id = None
#         if self.request.user.is_authenticated:
#             user_id = self.request.user.id

#         has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()

#         if not has_been_visited:
#             new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
#             new_visit.save()

#         return context

class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        
        # +++ دریافت قیمت روز طلا از ماژول tablo +++
        gold_data = get_gold_prices()
        gold_18k_price_str = gold_data.get('gold_prices', {}).get('طلا 18 عیار', '0')
        # تبدیل قیمت رشته‌ای به عدد (حذف کاما)
        try:
            GOLD_BASE_PRICE = int(''.join(filter(str.isdigit, str(gold_18k_price_str))))
        except:
            GOLD_BASE_PRICE = 12500000  # مقدار پیش‌فرض ایمن
        
        # +++ محاسبه قیمت نهایی محصول +++
        price_details = loaded_product.calculate_final_price(GOLD_BASE_PRICE)
        
        # +++ ارسال داده‌های جدید به تمپلیت +++
        context['price_details'] = price_details
        context['gold_base_price'] = GOLD_BASE_PRICE
        context['gold_last_updated'] = gold_data.get('last_updated', '')
        
        # بقیه کدهای قبلی (بدون تغییر)
        favorite_product_id = request.session.get("product_favorites")
        context['is_favorite'] = favorite_product_id == str(loaded_product.id)
        context['banners'] = SiteBanner.objects.filter(is_active=True, position__iexact=SiteBanner.SiteBannerPositions.product_detail)
        galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id).all())
        galleries.insert(0, loaded_product)
        context['product_galleries_group'] = group_list(galleries, 3)
        context['related_products'] = group_list(list(Product.objects.filter(brand_id=loaded_product.brand_id).exclude(pk=loaded_product.id).all()[:12]), 3)
        
        # بازدید (بدون تغییر)
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()

        return context


class AddProductFavorite(View):
    def post(self, request):
        product_id = request.POST["product_id"]
        product = Product.objects.get(pk=product_id)
        request.session["product_favorites"] = product_id
        return redirect(product.get_absolute_url())


def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'categories': product_categories
    }
    return render(request, 'product_module/components/product_categories_component.html', context)


def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brands
    }
    return render(request, 'product_module/components/product_brands_component.html', context)
