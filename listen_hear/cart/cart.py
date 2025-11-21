"""Cart session management utility"""
from decimal import Decimal
from django.conf import settings

from listen_hear.packages.models import PackageTemplate


class Cart:
    """Session-based shopping cart"""

    def __init__(self, request):
        """Initialize the cart"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, package, quantity=1, override_quantity=False):
        """
        Add a package to the cart or update its quantity.
        """
        package_id = str(package.id)
        if package_id not in self.cart:
            self.cart[package_id] = {
                'quantity': 0,
                'price_low': str(package.price_low),
                'price_high': str(package.price_high),
                'name': package.name,
            }
        if override_quantity:
            self.cart[package_id]['quantity'] = quantity
        else:
            self.cart[package_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Mark the session as modified to ensure it's saved"""
        self.session.modified = True

    def remove(self, package):
        """Remove a package from the cart"""
        package_id = str(package.id)
        if package_id in self.cart:
            del self.cart[package_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the packages
        from the database.
        """
        package_ids = self.cart.keys()
        # Get the package objects and add them to the cart
        packages = PackageTemplate.objects.filter(id__in=package_ids)
        cart = self.cart.copy()
        for package in packages:
            cart[str(package.id)]['package'] = package

        for item in cart.values():
            item['price_low'] = Decimal(item['price_low'])
            item['price_high'] = Decimal(item['price_high'])
            item['total_low'] = item['price_low'] * item['quantity']
            item['total_high'] = item['price_high'] * item['quantity']
            yield item

    def __len__(self):
        """Count all items in the cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_low(self):
        """Calculate the total low price of items in the cart"""
        return sum(Decimal(item['price_low']) * item['quantity']
                   for item in self.cart.values())

    def get_total_high(self):
        """Calculate the total high price of items in the cart"""
        return sum(Decimal(item['price_high']) * item['quantity']
                   for item in self.cart.values())

    def clear(self):
        """Remove cart from session"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
