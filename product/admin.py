from django.contrib import admin
from .models import product_category, product, ingredient

admin.site.register(product.Product)
admin.site.register(product_category.ProductCategory)
admin.site.register(ingredient.ProductIngredient)
