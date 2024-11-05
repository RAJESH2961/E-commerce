from django.contrib import admin
from .models import * #It will import all models in the model file

admin.site.register(ContactForm)

# overdiding the admin model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image','description') 
# Register your models here.
admin.site.register(Category,CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    # list_display = ('name', 'quantity','selling_price','trending')
    list_display = ('name', 'vendor', 'category', 'status', 'trending', 'selling_price', 'created_at')
    list_filter = ('status', 'trending', 'category')
admin.site.register(Product,ProductAdmin)
# admin.site.register(Review)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'is_approved', 'sentiment', 'confidence_score')
    list_filter = ('sentiment', 'is_approved', 'rating')
    # ordering = ('-confidence_score',)  # Order by confidence score, highest first
admin.site.register(Review, ReviewAdmin)




