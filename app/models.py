from django.db import models
# from django.contrib.auth.models import User
# in case if we  upload files multiple times single file it will overide so we create with current time with filename uses concatination to add current time and file name

import datetime #to get current time
import os #to access path

# This function accept the filename and returns current time with file and stores in uploads/
def getFileName(req,filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    description=models.TextField(max_length=500,null=False,blank=True)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# class Product(models.Model):
#     Category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     original_price = models.DecimalField(max_digits=10, decimal_places=2)
#     selling_price = models.DecimalField(max_digits=10, decimal_places=2)
#     product_image = models.ImageField(upload_to='products/')
#     quantity = models.IntegerField()
#     status = models.BooleanField(default=True)
#     trending = models.BooleanField(default=False)
#     vendor = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     # Other fields...

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150, null=False, blank=False)
    vendor = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    status = models.BooleanField(default=False, help_text="0-show, 1-Hidden")
    trending = models.BooleanField(default=False, help_text="0-default, 1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    # ordering = ['-created_at']: This specifies the default ordering for the model. Products will be ordered by created_at in descending order (newest first).
    class Meta:
        ordering = ['-created_at']