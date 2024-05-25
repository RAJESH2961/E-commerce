from django.contrib import admin
from .models import * #It will import all models in the model file

admin.site.register(ContactForm)

# overdiding the admin model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image','description') 
# Register your models here.
admin.site.register(Category,CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity','selling_price','trending')
admin.site.register(Product,ProductAdmin)





