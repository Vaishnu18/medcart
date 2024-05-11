import json

from django.http import JsonResponse
from django.shortcuts import render,redirect
from ecommerceapp.models import Contact,Product,Orders,OrderUpdate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from math import ceil
from .models import Product
def index(request):
    allProds = []
    catprods = Product.objects.values('category','id')
    print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params= {'allProds':allProds}

    return render(request,"index.html",params)

def search(request):
    query = request.GET.get('query')
    results = Product.objects.filter(product_name__icontains=query)
    context = {'results': results, 'query': query}
    return render(request, 'search_results.html', context)

def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

@login_required
def orders(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')

        if action == 'cancel':
            order = Orders.objects.filter(order_id=order_id, email=request.user.email).first()
            if order:
                order.delete()
                messages.success(request, 'Order canceled successfully.')

        elif action == 'return':
            order = Orders.objects.filter(order_id=order_id, email=request.user.email).first()
            if order:
                order.status = 'Return'
                order.save()
                messages.success(request, 'Order is returning.')

    orders = Orders.objects.filter(email=request.user.email)

    for order in orders:
        order_items = json.loads(order.items_json)

        for item_id, item_details in order_items.items():
            quantity, name, price = item_details
            item_name = name  # Retrieve the name

            # Add the item name to the order object
            order.item_name = item_name
            # Retrieve the latest OrderUpdate for the order
            order_update = OrderUpdate.objects.filter(order_id=order.order_id).latest('timestamp')

            # Add the timestamp (order date) to the order object
            order.order_date = order_update.timestamp

        # Add a property to indicate if the order can be canceled
        order.can_cancel = True  # Modify this condition based on your cancellation criteria

    context = {
        'orders': orders
    }

    return render(request, 'orders.html', context)




def checkout(request):
    
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auths/login')

    thank = False
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True
    return render(request,"checkout.html",{'thank': thank})
def payment(request):
    return render(request,"payment.html")





