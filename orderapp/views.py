from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Itemorder, Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.serializers import serialize
from django.db import IntegrityError

@login_required
def product_page(request):
    products = Product.objects.all()

    if request.method == 'POST':
        user = request.user
        order_date = request.POST['order_date']  # Date 

        for product_id in request.POST.getlist('selected_products'):
            # Fetch the quantity from the hidden input field
            quantity = int(request.POST.get(f'hidden_quantity_{product_id}', 1))  # Default is 1 
            special_instruction = request.POST.get(f'instruction_{product_id}', '')

            try:
                product = Product.objects.get(id=product_id)

                # Check if the same product was ordered by the same user on the same day
                order_exists = Itemorder.objects.filter(user=user, product=product, order_date=order_date).exists()

                if order_exists:
                    messages.error(request, f"You have already ordered {product.name} today. You cannot order the same item twice on the same day.")
                else:
                    # If not such any order exists, create the new order
                    Itemorder.objects.create(
                        user=user,
                        product=product,
                        quantity=quantity,
                        special_instruction=special_instruction,
                        order_date=order_date,
                        total_price=quantity * product.price
                    )
                    messages.success(request, f"Your order for {product.name} has been placed successfully!")

            except Product.DoesNotExist:
                messages.error(request, f"Product with ID {product_id} does not exist.")
                continue

    return render(request, 'all_products.html', {'products': products})







@login_required
def order_page(request):
    orders = Itemorder.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Itemorder, order_id=order_id, user=request.user)
    return render(request, 'order_list.html', {'order': order})
