from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import PackageTemplate, Category, SubCategory


def home(request):
    """Homepage with featured packages"""
    featured_packages = PackageTemplate.objects.filter(is_active=True)[:6]
    categories = Category.objects.filter(is_active=True)
    context = {
        'featured_packages': featured_packages,
        'categories': categories,
    }
    return render(request, 'pages/home.html', context)


class PackageListView(ListView):
    """List all active packages"""
    model = PackageTemplate
    template_name = 'packages/list.html'
    context_object_name = 'packages'
    paginate_by = 12

    def get_queryset(self):
        """Filter packages by active status"""
        return PackageTemplate.objects.filter(is_active=True).select_related('category', 'subcategory')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        return context


class PackageDetailView(DetailView):
    """Detail view for a single package"""
    model = PackageTemplate
    template_name = 'packages/detail.html'
    context_object_name = 'package'

    def get_queryset(self):
        """Only show active packages"""
        return PackageTemplate.objects.filter(is_active=True).select_related(
            'category', 'subcategory', 'requires_phase'
        ).prefetch_related('install_phases')


class CategoryPackageListView(ListView):
    """List packages by category"""
    model = PackageTemplate
    template_name = 'packages/category_list.html'
    context_object_name = 'packages'
    paginate_by = 12

    def get_queryset(self):
        """Filter packages by category"""
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'], is_active=True)
        queryset = PackageTemplate.objects.filter(
            category=self.category,
            is_active=True
        ).select_related('category', 'subcategory')

        # Filter by subcategory if provided
        subcategory_id = self.request.GET.get('subcategory')
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['subcategories'] = SubCategory.objects.filter(
            category=self.category,
            is_active=True
        )
        return context
