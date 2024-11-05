from django.shortcuts import render,redirect
from django.http import  JsonResponse

from .models import *
from django.contrib import messages#we can use it in anywhere in the application globally 
from django.http import HttpResponse
from .form import *
from django.contrib.auth import authenticate,login,logout
from Ecommerce import settings
from django.core.mail import EmailMessage

# Create your views here.

# def home(req):
#     products=Product.objects.filter(trending=1)
#     return render(req, 'index.html', {'products':products})
from .models import Product, Category

def home(req):
    # Attempt to get the "Laptop" category
    laptop_category = Category.objects.filter(name="Laptops").first()

    # Fetch all trending products
    trending_products = Product.objects.filter(trending=True)[:12]

    # Fetch trending laptops if the category exists
    if laptop_category:
        trending_laptops = Product.objects.filter(trending=True, category=laptop_category)[:5]
    else:
        trending_laptops = []  # No trending laptops found

    return render(req, 'index.html', {
        'products': trending_products,
        'trending_laptops': trending_laptops
    })


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
                return redirect('success')
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
from .models import Category, Product, Review
from django.shortcuts import render, redirect
from django.contrib import messages
from transformers import pipeline

# Initialize the sentiment analyzer
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=0)  # Use device=0 for GPU, or device=-1 for CPU

def product_details(req, cname, pname):
    # Check if the category exists and is active
    if Category.objects.filter(name=cname, status=0).exists():
        # Check if the product exists and is active
        if Product.objects.filter(name=pname, status=0).exists():
            product = Product.objects.filter(name=pname, status=0).first()
            # Fetch only approved reviews
            reviews = product.reviews.filter(is_approved=True)

            # Handle the review submission
            if req.method == 'POST':
                rating = req.POST.get('rating')
                comment = req.POST.get('comment')

                # Check if the user is authenticated
                if req.user.is_authenticated:
                    if rating and comment:
                        try:
                            # Perform sentiment analysis
                            result = sentiment_analyzer(comment)[0]
                            sentiment = result['label'].lower()
                            confidence_score = result['score']

                            # Create a new review object and save it to the database
                            review = Review.objects.create(
                                product=product,
                                user=req.user,
                                rating=rating,
                                comment=comment,
                                is_approved=False,  # Set to False initially for admin approval
                                sentiment=sentiment,  # Save the sentiment analysis result
                                confidence_score=confidence_score,  # Save the confidence score
                            )
                            review.save()
                            
                            messages.success(req, "Your review has been submitted and is awaiting approval.")
                            return redirect('product_details', cname=cname, pname=pname)
                        except Exception as e:
                            messages.error(req, f"An error occurred while processing your review: {str(e)}")
                    else:
                        messages.error(req, "Please provide both rating and comment.")
                else:
                    messages.error(req, "You must be logged in to submit a review.")
                    return redirect('login_view')  # Redirect to login if not authenticated

            # Calculate overall sentiment for the product
            if reviews.exists():
                # Prepare review texts for analysis
                review_texts = [review.comment for review in reviews]
                results = sentiment_analyzer(review_texts)

                # Calculate overall sentiment
                positive_count = sum(1 for result in results if result['label'] == 'POSITIVE')
                negative_count = sum(1 for result in results if result['label'] == 'NEGATIVE')
                total_count = len(results)

                positive_percentage = (positive_count / total_count) * 100 if total_count > 0 else 0
                negative_percentage = (negative_count / total_count) * 100 if total_count > 0 else 0

                # Prepare data for the template
                sentiment_analysis = {
                    'positive_count': positive_count,
                    'negative_count': negative_count,
                    'positive_percentage': positive_percentage,
                    'negative_percentage': negative_percentage,
                    'total_reviews': total_count,
                }
            else:
                sentiment_analysis = None

            # Render the product details template with product, reviews, and sentiment analysis
            return render(req, "products/product_details.html", {
                "products": product,
                "reviews": reviews,
                "sentiment_analysis": sentiment_analysis,
            })
        else:
            messages.error(req, "No such product found.")
            return redirect('collections')
    else:
        messages.error(req, "No such category found.")
        return redirect('collections')


def contact(req):
    if req.method=="POST":
        name = req.POST['name']
        email = req.POST['email']
        number = req.POST['mobile']
        subject = req.POST['subject']
        message = req.POST['message']
        user=ContactForm(name=name, email=email, mobile=number, subject=subject, message=message)
        user.save()
        sub="welcome"
        body="Hi"
        sender=settings.EMAIL_HOST_USER
        receiver=email
        email_msg=EmailMessage(sub,body,sender,[receiver])
        if email_msg==1:
            print("Send Successfully")
        else :
            print("failed")
        return redirect('success')
    else:
        return render(req,'contact/contact.html')
    
def success(req):
    return render(req,'contact/success.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .form import CustomUserChangeForm

@login_required
def updateprofile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('success')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'updateprofile.html', {'form': form})


from django.contrib.auth import update_session_auth_hash

from .form import CustomPasswordChangeForm

@login_required
def changepassword(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session with the new password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login_view')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'changepassword.html', {'form': form})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product, Cart

@csrf_exempt  # Temporarily add this if you are testing without CSRF tokens (not recommended in production)
def add_to_cart(request):
    print("Entered add_to_cart view")  # Debugging statement
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("Request is AJAX")
        if request.user.is_authenticated:
            print("User is authenticated")
            data = json.load(request)
            product_qty = data.get('product_qty')
            product_id = data.get('pid')
            print("Product ID:", product_id, "Quantity:", product_qty)

            print("Product ID:", product_id)          # Debugging
            print("Product Quantity:", product_qty)   # Debugging
            print("User ID:", request.user.id)        # Debugging

            try:
                product = Product.objects.get(id=product_id)
                if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                    return JsonResponse({'status': 'Product Already in Cart'}, status=200)
                else:
                    if product.quantity >= product_qty:
                        Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                        return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
            except Product.DoesNotExist:
                return JsonResponse({'status': 'Product Not Found'}, status=404)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=401)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)


def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"cart.html",{"cart":cart})
  else:
    return redirect("/")

def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")

