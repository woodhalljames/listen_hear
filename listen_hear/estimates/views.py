from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from listen_hear.cart.cart import Cart
from listen_hear.packages.models import PackageTemplate
from .models import Estimate, EstimateItem
from .forms import EstimateCreateForm, GuestCheckoutForm


def checkout(request):
    """Checkout view - handles both authenticated and guest checkout"""
    cart = Cart(request)

    # Check if cart is empty
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('packages:list')

    # If user is authenticated, use simple form
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EstimateCreateForm(request.POST)
            if form.is_valid():
                estimate = create_estimate_from_cart(request, cart, form)
                if estimate:
                    cart.clear()
                    messages.success(request, f'Estimate {estimate.estimate_number} created successfully!')
                    return redirect('estimates:thank_you', estimate_number=estimate.estimate_number)
        else:
            form = EstimateCreateForm()

        context = {
            'form': form,
            'cart': cart,
        }
        return render(request, 'estimates/checkout.html', context)

    # Guest checkout
    else:
        if request.method == 'POST':
            form = GuestCheckoutForm(request.POST)
            if form.is_valid():
                estimate = create_guest_estimate_from_cart(request, cart, form)
                if estimate:
                    cart.clear()
                    messages.success(request, f'Estimate {estimate.estimate_number} created successfully!')
                    return redirect('estimates:thank_you', estimate_number=estimate.estimate_number)
        else:
            form = GuestCheckoutForm()

        context = {
            'form': form,
            'cart': cart,
        }
        return render(request, 'estimates/guest_checkout.html', context)


def create_estimate_from_cart(request, cart, form):
    """Helper function to create estimate for authenticated user"""
    with transaction.atomic():
        estimate = form.save(commit=False)
        estimate.builder = request.user
        estimate.total_low = cart.get_total_low()
        estimate.total_high = cart.get_total_high()
        estimate.save()

        # Create estimate items
        for item in cart:
            EstimateItem.objects.create(
                estimate=estimate,
                package=item['package'],
                price_low_snapshot=item['price_low'],
                price_high_snapshot=item['price_high'],
                package_name_snapshot=item['name']
            )

        return estimate


def create_guest_estimate_from_cart(request, cart, form):
    """Helper function to create estimate for guest user"""
    from listen_hear.users.models import User

    with transaction.atomic():
        # Get or create guest user based on email
        email = form.cleaned_data['email']
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'company_name': form.cleaned_data['company_name'],
                'contact_person': form.cleaned_data['contact_person'],
                'phone': form.cleaned_data.get('phone', ''),
            }
        )

        # Update user info if exists
        if not created:
            user.company_name = form.cleaned_data['company_name']
            user.contact_person = form.cleaned_data['contact_person']
            if form.cleaned_data.get('phone'):
                user.phone = form.cleaned_data['phone']
            user.save()

        # Create estimate
        estimate = Estimate.objects.create(
            builder=user,
            client_name=form.cleaned_data.get('client_name', ''),
            client_email=form.cleaned_data.get('client_email', ''),
            notes=form.cleaned_data.get('notes', ''),
            total_low=cart.get_total_low(),
            total_high=cart.get_total_high()
        )

        # Create estimate items
        for item in cart:
            EstimateItem.objects.create(
                estimate=estimate,
                package=item['package'],
                price_low_snapshot=item['price_low'],
                price_high_snapshot=item['price_high'],
                package_name_snapshot=item['name']
            )

        return estimate


def thank_you(request, estimate_number):
    """Thank you page after estimate creation"""
    estimate = get_object_or_404(Estimate, estimate_number=estimate_number)
    context = {
        'estimate': estimate,
    }
    return render(request, 'estimates/thank_you.html', context)


@login_required
def dashboard(request):
    """Builder dashboard showing all their estimates"""
    estimates = Estimate.objects.filter(builder=request.user).prefetch_related('items')
    context = {
        'estimates': estimates,
    }
    return render(request, 'estimates/dashboard.html', context)


@login_required
def estimate_detail(request, estimate_number):
    """View a single estimate detail"""
    estimate = get_object_or_404(
        Estimate.objects.prefetch_related('items__package'),
        estimate_number=estimate_number,
        builder=request.user
    )
    context = {
        'estimate': estimate,
    }
    return render(request, 'estimates/detail.html', context)
