from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages#we can use it in anywhere in the application globally 
from django.http import HttpResponse
from .form import *
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def home(req):
    products=Product.objects.filter(trending=1)
    return render(req, 'index.html', {'products':products})

# def register(req):
#     form=RegisterForm()
#     if req.method == 'POST':
#              form=RegisterForm(req.POST)
#              if form.is_valid:
#                   form.save()
#                   messages.success(req,'Registration Success You can LOgin Now')
#                   return redirect('login')
#              else:
#                   print(form.errors)    
#     return render(req, 'register.html', {'form':form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request,'Registration Success You can Login Now')
                return redirect('login_view')
            except ValueError as e:
                print(f"Error saving user: {e}")
                print(form.errors)  # Print form errors to the console
        else:
            print(form.errors)  # Print form errors to the console
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(req):
    # this below code is activated wheh the user is loggedin to application but but when they tried /login_view in url of the webpage it will redirect to login eventhough when they are aldready logged in
    #so here we are redirecting to home page when user is authenticated such as loggedin
    if req.user.is_authenticated:
        return redirect('home')
    else:
        if req.method=="POST":
            name=req.POST.get('username')#It will get the username from the form ex:name=username
            pwd=req.POST.get('password')#It will get the pasword from the login form ex:name:password
            user=authenticate(req,username=name,password=pwd)#It will create a session
            if user is not None:#It will check the credentials in the database if it is valid ie Not None
                login(req,user)
                messages.success(req,"Logged in Successfully ! ")
                return redirect('home')
            else:
                messages.error(req,"User Name Not Found ")
                return redirect('login_view')
        return render(req, 'login.html')

def logout_view(req):
    if req.user.is_authenticated:
        logout(req)
        messages.success(req,"Logged out Succesfully ")
        req.session['just_logged_out'] = True
        return redirect('home')


def collections(req):
    collection=Category.objects.filter(status=0)
    return render(req, 'collections.html',{"item" : collection})

def collections_view(req,name):
    if Category.objects.filter(name=name, status=0).exists():
        # Product.objects.filter(category__name=name) filters the products by the related category's name using a double underscore __ to traverse the foreign key relationship.
        products = Product.objects.filter(category__name=name)
        return render(req, 'products/collections_view.html', {"products": products,'category_name':name})

    else:
        messages.warning(req, "No such Category found")
        return redirect('collections')

def product_details(req,cname,pname):
    if Category.objects.filter(name=cname, status=0):
            if Product.objects.filter(name=pname, status=0):
                 products=Product.objects.filter(name=pname,status=0).first()
                 return render(req,"products/product_details.html",{"products":products})
            else:
                 messages.error(req,"No such product Found ")
                 return redirect('collections')
    else:
         messages.error(req,"No such Category Found")
         return redirect('collections')
         



