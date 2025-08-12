from django.contrib import admin
from contact import models

# Register your models here.

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = 'first_name', 'last_name', 'phone', 'category_name', 'show',
    ordering = '-id', 'first_name'
    search_fields = 'first_name', 'last_name', 'phone', 'email',
    list_per_page = 10
    list_max_show_all = 25
    list_display_links = 'first_name',
    list_editable = "show",
    
    def category_name(self, obj):
        return obj.category.category_name if obj.category else '-'
    category_name.admin_order_field = 'category__name'  # Allows to sort by Category
    category_name.short_description = 'Category'       # Column name in the admin panel


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'category_name',
    list_display_links= 'id',
    ordering = '-id', 'category_name',
    search_fields = 'category_name',
    list_editable = 'category_name',
