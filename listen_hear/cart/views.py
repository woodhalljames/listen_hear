from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from listen_hear.packages.models import PackageTemplate
from .cart import Cart


def cart_detail(request):
    """Display the cart"""
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_add(request, package_id):
    """Add a package to the cart"""
    cart = Cart(request)
    package = get_object_or_404(PackageTemplate, id=package_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(package=package, quantity=quantity)
    messages.success(request, f'{package.name} added to your cart.')

    # Redirect to the referring page or cart detail
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', 'cart:cart_detail'))
    return redirect(next_url)


@require_POST
def cart_remove(request, package_id):
    """Remove a package from the cart"""
    cart = Cart(request)
    package = get_object_or_404(PackageTemplate, id=package_id)
    cart.remove(package)
    messages.info(request, f'{package.name} removed from your cart.')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, package_id):
    """Update package quantity in cart"""
    cart = Cart(request)
    package = get_object_or_404(PackageTemplate, id=package_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart.add(package=package, quantity=quantity, override_quantity=True)
        messages.success(request, f'Cart updated.')
    else:
        cart.remove(package)
        messages.info(request, f'{package.name} removed from your cart.')

    return redirect('cart:cart_detail')
