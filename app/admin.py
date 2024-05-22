from django.contrib import admin
from .models import * #It will import all models in the model file

# overdiding the admin model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image','description')


    
# Register your models here.
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product)
# admin.site.register(mobile)


