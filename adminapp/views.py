from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserRegisterForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/создание'
        return context


class UserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/список'
        return context

    def get_ordering(self):
        self.ordering = ('-is_active', '-is_superuser', '-is_staff', 'username')
        return self.ordering


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        return context


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/удаление'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object.is_active = True
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context


class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    paginate_by = 3

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/список'
        return context

    def get_ordering(self):
        self.ordering = ('pk')
        return self.ordering

    # def get_queryset(self):
    #     return super().get_queryset().filter(is_active=True)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/удаление'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
            self.object.save()
            products = Product.objects.filter(category_id=self.object.pk)
            for product in products:
                product.is_active = False
                product.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object.is_active = True
            self.object.save()
            products = Product.objects.filter(category_id=self.object.pk)
            for product in products:
                product.is_active = True
                product.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты/список'
        category_item = self.kwargs.get('pk', None)
        if category_item is not None:
            category = ProductCategory.objects.get(pk=category_item)
            context['category'] = category
            return context
        return context

    def get_queryset(self):
        category = self.kwargs.get('pk', None)
        if category is not None:
            products = Product.objects.filter(category_id=category)
            return products
        return Product.objects.all()


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:products')
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/создание'
        category_item = self.kwargs.get('pk', None)
        if category_item is not None:
            category = ProductCategory.objects.get(pk=category_item)
            context['category'] = category
            context['form']['category'].initial = category
            return context
        return context

    def get_success_url(self):
        category_pk = self.object.category.pk
        return reverse_lazy('admin:products', kwargs={'pk': category_pk})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/просмотр'
        return context


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:products')
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/редактирование'
        category_item = self.object.category.pk

        if category_item is not None:
            category = ProductCategory.objects.get(pk=category_item)
            context['category'] = category
            return context
        return context

    def get_success_url(self):
        category_pk = self.object.category.pk
        return reverse_lazy('admin:products', kwargs={'pk': category_pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('admin:products')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/удаление'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object.is_active = True
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        category_pk = self.object.category.pk
        return reverse_lazy('admin:products', kwargs={'pk': category_pk})


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)

# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'пользователи/создание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     content = {
#         'title': title,
#         'update_form': user_form,
#     }
#     return render(request, 'adminapp/user_update.html', content)

# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     content = {
#         'title': title,
#         'objects': users_list
#     }
#     return render(request, 'adminapp/users.html', content)

# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'пользователи/редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
#     else:
#         user_form = ShopUserAdminEditForm(instance=edit_user)
#
#     content = {
#         'title': title,
#         'update_form': user_form,
#     }
#     return render(request, 'adminapp/user_update.html', content)

# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'пользователи/удаление'
#
#     user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('admin:users'))
#
#     content = {
#         'title': title,
#         'user_to_delete': user,
#     }
#     return render(request, 'adminapp/user_delete.html', content)

# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категории/создание'
#
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         category_form = ProductCategoryEditForm()
#
#     content = {
#         'title': title,
#         'update_form': category_form,
#     }
#     return render(request, 'adminapp/category_update.html', content)

# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'
#
#     categories_list = ProductCategory.objects.all()
#
#     content = {
#         'title': title,
#         'objects': categories_list,
#     }
#     return render(request, 'adminapp/categories.html', content)

# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категории/редактирование'
#
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES, instance=category_item)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:category_update', args=[category_item.pk]))
#     else:
#         category_form = ProductCategoryEditForm(instance=category_item)
#
#     content = {
#         'title': title,
#         'update_form': category_form,
#     }
#     return render(request, 'adminapp/category_update.html', content)

# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if category_item.is_active == True:
#         if request.method == 'POST':
#             category_item.is_active = False
#             category_item.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         if request.method == 'POST':
#             category_item.is_active = True
#             category_item.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     content = {
#         'title': title,
#         'category_to_delete': category_item,
#     }
#     return render(request, 'adminapp/category_delete.html', content)

# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     title = 'продукты'
#
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category=category_item).order_by('name')
#
#     content = {
#         'title': title,
#         'objects': products_list,
#         'category': category_item
#     }
#     return render(request, 'adminapp/products.html', content)

# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'продукт/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#     content = {
#         'title': title,
#         'object': product,
#     }
#     return render(request, 'adminapp/product_read.html', content)

# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     title = 'продукт/создание'
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[pk]))
#     else:
#         product_form = ProductEditForm(initial={'category': category})
#
#     content = {
#         'title': title,
#         'update_form': product_form,
#         'category': category
#     }
#     return render(request, 'adminapp/product_update.html', content)

# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     title = 'продукт/редактирование'
#     product_item = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES, instance=product_item)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin:product_update', args=[product_item.pk]))
#     else:
#         product_form = ProductEditForm(instance=product_item)
#
#     content = {
#         'title': title,
#         'update_form': product_form,
#         'category': product_item.category
#     }
#     return render(request, 'adminapp/product_update.html', content)

# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     title = 'продукт/удаление'
#
#     product_item = get_object_or_404(Product, pk=pk)
#     print(product_item.category.pk)
#     if product_item.is_active == True:
#         if request.method == 'POST':
#             product_item.is_active = False
#             product_item.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[product_item.category.pk]))
#     else:
#         if request.method == 'POST':
#             product_item.is_active = True
#             product_item.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[product_item.category.pk]))
#
#     content = {
#         'title': title,
#         'product_to_delete': product_item,
#     }
#
#     return render(request, 'adminapp/product_delete.html', content)
