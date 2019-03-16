# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView 
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.urls import reverse_lazy

from .models import Product
from .forms import ProductForm

def index(request):
    return HttpResponse("Hello, world.")

class ProductList(ListView):
    """Product list generic views"""" 
    model = Product

class ProductDetail(DetailView):
    """Product detail generic views""""  
    model = Product

class ProductCreate(SuccessMessageMixin, CreateView):
    """Product create generic views""""  
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    success_message = "Product successfully created!"

class ProductUpdate(SuccessMessageMixin, UpdateView): 
    """Product update generic views"""" 
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    success_message = "Product successfully updated!"

class ProductDelete(SuccessMessageMixin, DeleteView): 
    """Product delete generic views"""" 
    model = Product
    success_url = reverse_lazy('product_list')
    success_message = "Product successfully deleted!"


