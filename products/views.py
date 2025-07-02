# marketplace_project/products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.contrib import messages

def product_list(request):
    # Start with all active products
    products = Product.objects.filter(is_active=True).select_related('category', 'seller')
    
    query = request.GET.get('q') # Get the search query from the URL parameter 'q'
    if query:
        # Filter products where name OR description contains the query (case-insensitive)
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
        
        # Add a message if no products are found for the search query
        if not products.exists():
            messages.info(request, f"No products found for '{query}'.")
        else:
            messages.info(request, f"Showing search results for '{query}'.")

    context = {
        'products': products, # This is the filtered queryset (or all products if no query)
        'query': query # Pass the query back to the template to pre-fill the search bar
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, f'Product "{product.name}" listed successfully!')
            # CHANGED: Redirect to product_list instead of product_detail
            return redirect('product_list') # <--- THIS IS THE CHANGE
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'List a New Product'})

@login_required
def my_products(request):
    my_listed_products = Product.objects.filter(seller=request.user).select_related('category', 'seller')
    context = {
        'products': my_listed_products,
        'title': 'My Listed Products'
    }
    return render(request, 'products/my_products.html', context)

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)

    # Ensure only the seller can update their product
    if product.seller.pk != request.user.pk:
        messages.error(request, "You are not authorized to edit this product.")
        return redirect('product_detail', pk=product.pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'title': f'Edit {product.name}'
    }
    return render(request, 'products/product_form.html', context)

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)

    # Ensure only the seller can delete their product
    if product.seller.pk != request.user.pk:
        messages.error(request, "You are not authorized to delete this product.")
        return redirect('product_detail', pk=product.pk)

    if request.method == 'POST':
        product_name = product.name # Store name before deleting
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully.')
        return redirect('my_products') # Redirect to 'my_products' after deletion
    
    context = {
        'product': product,
        'title': f'Confirm Delete: {product.name}'
    }
    return render(request, 'products/product_confirm_delete.html', context)
