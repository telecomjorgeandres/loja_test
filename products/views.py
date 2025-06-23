from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q # For search, introduced later

def product_list(request):
        # This view will become problematic with many products (N+1 query)
        products = Product.objects.filter(is_active=True).select_related('category', 'seller')
        context = {'products': products}
        return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
        product = get_object_or_404(Product, pk=pk, is_active=True)
        context = {'product': product}
        return render(request, 'products/product_detail.html', context)

@login_required # Only logged-in users can create products
def product_create(request):
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.seller = request.user
                product.save()
                return redirect('product_detail', pk=product.pk) # Bug: no success message
        else:
            form = ProductForm()
        return render(request, 'products/product_create.html', {'form': form})
