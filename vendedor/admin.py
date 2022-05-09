from django.contrib import admin
from .models import Product, Category, Report, ReportDetail


class ReportAdmin(admin.ModelAdmin):
    list_display = ('user','date')

class ReportDetailAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'product_id', 'quantity', 'price', 'commission_paid', 'commission_receivable', 'total')

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('category_id','name','price','commission')
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)

admin.site.register(Product)
admin.site.register(Report, ReportAdmin)
admin.site.register(ReportDetail,ReportDetailAdmin)