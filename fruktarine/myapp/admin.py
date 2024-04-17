from typing import List

from django.contrib import admin
from .models import Product, Order, OrderItem

@admin.action(description="Сбросить количество в ноль")
def reset_quantity(modeladmin, request, queryset):
    queryset.update(quantity=0)

@admin.action(description="Установить статус 'Оплачен'")
def mark_as_paid(modeladmin, request, queryset):
    queryset.update(status='Paid')

@admin.action(description="Удалить из корзины")
def delete_from_cart(modeladmin, request, queryset):
    queryset.update(quantity=0)

@admin.action(description="Создать новый заказ")
def create_new_order(modeladmin, request, queryset):
    total_price = sum(item.price for item in queryset)
    new_order = Order.objects.create(total_price=total_price)
    new_order.items.set(queryset)


@admin.action(description="Добавить скидку")
def add_discount(modeladmin, request, queryset):
    for item in queryset:
        item.price -= item.price * 0.1  # Пример скидки 10%
        item.save()

class ProductAdmin(admin.ModelAdmin):
    """Список продуктов."""
    list_display = ['title', 'price', 'quantity', 'date_added', 'available']
    list_filter = ['price', 'quantity', 'date_added', 'available']
    search_fields = ['title', 'description']
    search_help_text = 'Поиск по полю Описание продукта (description)'
    actions = [reset_quantity]
    list_per_page = 10
    """Отдельный продукт."""
    # fields = ['name', 'description', 'category', 'date_added', 'rating'] #определяет порядок вывода элементов формы
    readonly_fields = ['date_added', 'rating']
    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['title'],
            },
        ),
        (
            'Подробности',
            {
                'classes': ['collapse'],
                'description': 'Категория товара и его подробное описание',
                'fields': ['description'],
            },
        ),
        (
            'Бухгалтерия',
            {
                'fields': ['price', 'quantity'],
            }
        ),
        (
            'Рейтинг и прочее',
            {
                'description': 'Рейтинг сформирован автоматически на основе оценок покупателей',
                'fields': ['rating', 'date_added'],
            }
        ),
    ]

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'date_added', 'username', 'email', 'address', 'delivery_date', 'total_price']
    list_filter = ['date_added', 'delivery_date']
    search_fields = ['username', 'email']
    list_per_page = 10

class OrderAdmin(admin.ModelAdmin):
    """Заказы."""
    list_display = ['id', 'date_added', 'username', 'email', 'address', 'delivery_date', 'total_price']
    list_filter = ['date_added', 'delivery_date']
    search_fields = ['username', 'email']

class OrderItemAdmin(admin.ModelAdmin):
    """Позиции заказа."""
    list_display = ['order', 'product', 'quantity', 'price_per_product']
    list_filter = ['quantity', 'price_per_product']
    search_fields = ['order__username', 'product__title']
    list_per_page = 10


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
