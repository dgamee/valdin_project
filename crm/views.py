# paths and models
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from .models import Client, Product, Activity
from .forms import ProductForm, ClientForm
import json


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class DashboardListView(LoginRequiredMixin, ListView):
    template_name = "dashboard.html"
    context_object_name = 'latest'
    paginate_by = 3

    def get_queryset(self):
        # Combine the latest clients and products efficiently
        clients = Client.objects.order_by('-id')[:3]
        products = Product.objects.all()[:3]
        return list(clients) + list(products)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'latest_product': Product.objects.order_by('-id')[:6],
            'latest_client': Client.objects.order_by('-id')[:3],
            'client_count': Client.objects.count(),
            'product_count': Product.objects.count(),
            'latest_activities': self.latest_activities(),
            'data': json.dumps([
                {'name': product.name, 'quantity_left': product.quantity_left}
                for product in Product.objects.order_by('-id')[:6]
            ]),
        })
        return context

    def latest_activities(self):
        return Activity.objects.order_by('-timestamp')[:10]


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class CreateClientView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/client/client_create.html"
    success_url = reverse_lazy('list_client')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Client: {self.object.name} was added successfully')
        Activity.objects.create(user=self.request.user, activity_type='Add Client', details=f'Added {self.object.name} as client')
        return response


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class ClientsListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "crm/client/client_list.html"
    paginate_by = 10
    queryset = Client.objects.all()


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "crm/client/client_detail.html"

    def dispatch(self, request, *args, **kwargs):
        client = self.get_object()
        Activity.objects.create(user=request.user, activity_type='View Client Detail', details=f'Viewed {client.name} profile')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/client/client_edit.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Client detail was edited successfully')
        Activity.objects.create(user=self.request.user, activity_type='Updated Client', details=f'Updated {self.object.name} client profile')
        return response


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "crm/client/client_delete.html"
    success_url = reverse_lazy("list_client")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Client detail was deleted successfully.')
        return response


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class CreateProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "crm/product/product_create.html"
    success_url = reverse_lazy('list_product')

    def form_valid(self, form):
        other_images = self.request.FILES.getlist('other_images')
        for image in other_images:
            print(image.name)
        response = super().form_valid(form)
        messages.success(self.request, f'Product: {self.object.name} was added successfully')
        Activity.objects.create(user=self.request.user, activity_type='Add Product', details=f'Added {self.object.name} as product')
        return response


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class ProductsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "crm/product/product_list.html"
    context_object_name = "products"
    paginate_by = 12
    queryset = Product.objects.all()


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'crm/product/product_edit.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Product detail was updated successfully')
        Activity.objects.create(user=self.request.user, activity_type='Updated Product', details=f'Updated {self.object.name} product profile')
        return response


    def form_invalid(self, form):
        # Add all form errors to the messages framework
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        
        # Render the invalid form with errors
        return super().form_invalid(form)

@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "crm/product/product_detail.html"

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        Activity.objects.create(user=request.user, activity_type='View Product Detail', details=f'Viewed {product.name} product profile')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "crm/product/product_delete.html"
    success_url = reverse_lazy("list_product")


class AddToCartView(LoginRequiredMixin, View):
    def get_queryset(self):
        return Product.objects.filter(quantity_left__gt=0)

    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('id')
        product_quantity = request.GET.get('quantity')
        product_price = request.GET.get('product_price')

        # Validate input parameters
        if not product_id or not product_quantity or not product_price:
            messages.error(request, 'Missing product data')
            return JsonResponse({'error': 'Missing product data'}, status=400)

        try:
            product_quantity = int(product_quantity)
        except ValueError:
            messages.error(request, 'Invalid quantity')
            return JsonResponse({'error': 'Invalid quantity'}, status=400)

        try:
            # Remove any commas from the price string before converting to float
            product_price = float(product_price.replace(',', ''))
        except ValueError:
            messages.error(request, 'Invalid price')
            return JsonResponse({'error': 'Invalid price'}, status=400)

        # Retrieve product from queryset
        try:
            product = self.get_queryset().get(pk=product_id)
        except Product.DoesNotExist:
            messages.error(request, 'Product does not exist or is not available')
            return JsonResponse({'error': 'Product does not exist or is not available'}, status=404)

        # Check if requested quantity exceeds available stock
        if product_quantity > product.quantity_left:
            messages.error(request, 'Requested quantity exceeds available stock')
            return JsonResponse({'error': 'Requested quantity exceeds available stock'}, status=400)

        # Initialize cart product
        cart_product = {
            str(product_id): {
                'id' : product_id,
                'name': product.name,
                'quantity': product_quantity,
                'price': product_price,
                'image_url': product.image.url,
                'description': product.description,
                'quantity_left': product.quantity_left
            }
        }
        # Retrieve cart data from session or initialize new cart
        cart_data = request.session.get('cart_data_obj', {})

        if str(product_id) in cart_data:
            cart_data[str(product_id)]['quantity'] += product_quantity
        else:
            cart_data.update(cart_product)

        # Update session data
        request.session['cart_data_obj'] = cart_data

        messages.success(request, 'Product added to cart successfully')
        return JsonResponse({
            'data': cart_data,
            'totalcartitems': len(cart_data)
        })
    
@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve cart data from session or initialize an empty cart
        cart_data = self.request.session.get('cart_data_obj', {})
        
        # Calculate total price and total quantity of items in the cart
        total_price = sum(item.get('quantity', 0) * item.get('price', 0) for item in cart_data.values())
        total_quantity = sum(item.get('quantity', 0) for item in cart_data.values())
        
        context['cart_data'] = cart_data
        context['total_price'] = total_price
        context['total_quantity'] = total_quantity
        
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        new_quantity = int(request.POST.get('new_quantity', 0))

        # Validate action and product_id
        if action not in ['update_quantity', 'checkout']:
            return JsonResponse({'error': 'Invalid action specified.'}, status=400)
        
        if not product_id:
            return JsonResponse({'error': 'Product ID is required.'}, status=400)
        
        # Retrieve product from database to check stock quantity
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)
        
        # Retrieve cart data from session
        cart_data = request.session.get('cart_data_obj', {})
        
        # Perform action based on the specified action
        if action == 'update_quantity':
            # Validate new_quantity
            if new_quantity <= 0:
                messages.error(request, 'Quantity must be greater than zero.')
                return JsonResponse({'error': 'Quantity must be greater than zero.'}, status=400)
            
            # Check if requested quantity exceeds available stock
            if new_quantity > product.quantity_left:
                messages.error(request, f'Quantity exceeds available stock ({product.quantity_left}).')
                return JsonResponse({'error': f'Quantity exceeds available stock ({product.quantity_left}).'}, status=400)
            
            # Update quantity of the specified product in the cart
            if str(product_id) in cart_data:
                cart_data[str(product_id)]['quantity'] = new_quantity
            else:
                messages.error(request, 'Product not found in cart.')
                return JsonResponse({'error': 'Product not found in cart.'}, status=404)
            
            request.session['cart_data_obj'] = cart_data
            messages.success(request, 'Quantity updated successfully.')
            return JsonResponse({'message': 'Quantity updated successfully.'}, status=200)
        
        elif action == 'checkout':
            # Validate cart contents, process payment, etc.
            
            if not cart_data:
                return JsonResponse({'error': 'Cart is empty. Add items before checkout.'}, status=400)
            
            # Calculating total price and total quantity for validation
            total_price = sum(item.get('quantity', 0) * item.get('price', 0) for item in cart_data.values())
            total_quantity = sum(item.get('quantity', 0) for item in cart_data.values())
            
            # Validate the cart before checkout
            if total_quantity == 0:
                return JsonResponse({'error': 'Cart is empty. Add items before checkout.'}, status=400)
            
            # Clear the cart after processing (example: after checkout)
            request.session['cart_data_obj'] = {}
            
            messages.success(request, 'Cart processed successfully. Your order has been placed.')
    
            return JsonResponse({'message': 'Cart processed successfully'}, status=200)
        

class CartItemDeleteView(LoginRequiredMixin, DeleteView):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        
        # Ensure product_id is provided
        if not product_id:
            return JsonResponse({'error': 'No product ID provided.'}, status=400)

        # Retrieve cart data from session
        cart_data = request.session.get('cart_data_obj', {})

        # Check if product exists in cart data
        if product_id in cart_data:
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data
            messages.success(request, 'Product removed from cart successfully.')
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Product not found in cart.'}, status=404)
        
@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/cart/checkout.html'
    context_object_name = "products"
    paginate_by = 12
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve cart data from session
        cart_data = self.request.session.get('cart_data_obj')
        print()
        
        # Calculate total price and total quantity of items in the cart
        total_price = sum(item.get('quantity', 0) * item.get('price', 0) for item in cart_data.values())
        total_quantity = sum(item.get('quantity', 0) for item in cart_data.values())
        
        context['cart_data'] = cart_data
        context['total_price'] = total_price
        context['total_quantity'] = total_quantity
        
        return context