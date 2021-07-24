from django.db.models import query
from django.db.models import Avg
from django.shortcuts import render, HttpResponse, redirect
from .models import ProductSelling, like, SearchSugesstion, ReviewsRating
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from shop.templatetags import extras


# Create your views here.
def home(request):
    suggestions = ProductSelling.objects.values('name')
    allprod = []
    prod = ProductSelling.objects.values('category')
    cat = {item['category'] for item in prod}
    for c in cat:
        product = ProductSelling.objects.filter(category=c)
        allprod.append(product)
    context = {'allprod': allprod, 'suggestions': suggestions}

    return render(request, 'index.html', context)


def seller(request):
    suggestions = ProductSelling.objects.values('category')
    if request.method == "POST" and request.FILES['image']:
        name = request.POST['name']
        category = request.POST['category']
        price = request.POST['price']
        dec = request.POST['dec']
        image = request.FILES['image']
        product = ProductSelling(name=name, category=category, price=price, image=image, dec=dec)
        product.save()
        messages.success(request, "Your " + name + " added successfully ")

    return render(request, 'seller.html', {'suggestions': suggestions})


def checkout(request):
    return render(request, 'checkout.html')


def like_post(request, pid):
    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('post_id')
        post_obj = ProductSelling.objects.get(prod_id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        liked, created = like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if liked.value == 'Like':
                liked.value = 'Unlike'
            else:
                liked.value = 'Like'

        liked.save()

    return redirect('ProductView', pid=pid)


def like_home(request):
    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('post_id')
        post_obj = ProductSelling.objects.get(prod_id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        liked, created = like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if liked.value == 'Like':
                liked.value = 'Unlike'
            else:
                liked.value = 'Like'

        liked.save()

    return redirect('home')


def search(request):
    suggestions = ProductSelling.objects.values('name')

    search = request.GET['search']
    allprodname = ProductSelling.objects.filter(name__icontains=search)
    allprodcategory = ProductSelling.objects.filter(category__icontains=search)
    allproddec = ProductSelling.objects.filter(dec__icontains=search)

    product = allprodname.union(allprodcategory, allproddec)
    if product.count() == 0 or len(search) < 2:
        messages.warning(request, "No search results found. Please refine your query.")
    context = {'product': product, 'search': search, 'suggestions': suggestions}

    return render(request, 'search.html', context)


def handlesingup(request):

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        username = request.POST['name']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already exists!")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email id is already exists!")
            return redirect('home')

        if len(username) < 5:
            messages.error(request, " Your user name must be under 5 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, " Passwords do not match")
            return redirect('home')

        my_user = User.objects.create_user(username, email, pass1)
        my_user.first_name = fname
        my_user.last_name = lname
        my_user.save()
        messages.success(request, " Successfully signup please go and do login ")

        return redirect("home")
    else:
        return HttpResponse('404 error')


def handlelogin(request):
    if request.method == "POST":
        username1 = request.POST["username1"]
        password1 = request.POST["password1"]
        user = authenticate(username=username1, password=password1)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome to ' + username1)
            return redirect("home")
        else:
            messages.error(request, 'Please Enter Valid User Name And Password!')
            return redirect("home")

    else:
        return HttpResponse("404 erorr")


def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect("home")


def review(request, pid):
    if request.method == 'POST':
        name = request.user
        star = request.POST.get('star')
        review = request.POST.get('review')
        productId = request.POST.get('productId')
        product = ProductSelling.objects.get(prod_id=productId)
        parentId = request.POST.get('parentId')
        if parentId == "":
            review = ReviewsRating(name=name, product=product, star=star, review=review)
            review.save()
            messages.success(request, "Your comment has been posted successfully")
        else:

            parent = ReviewsRating.objects.get(id=parentId)
            review = ReviewsRating(name=name, product=product, star=star, review=review, parent=parent)
            review.save()
            messages.success(request, "Your reply has been posted successfully")

    return redirect('ProductView', pid=pid)


def productsView(request, pid):
    product = ProductSelling.objects.get(prod_id=pid)
    review = ReviewsRating.objects.filter(product=product, parent=None).order_by('-id')
    replies = ReviewsRating.objects.filter(product=product).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.id not in replyDict.keys():
            replyDict[reply.parent.id] = [reply]
        else:
            replyDict[reply.parent.id].append(reply)

    context = {'replyDict': replyDict,
               'product': product,
               'review': review, }

    return render(request, 'prodview.html', context)