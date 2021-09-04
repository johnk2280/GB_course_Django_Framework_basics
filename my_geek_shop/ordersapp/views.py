from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'ordersapp/orders.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemsCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = []
    template_name = 'ordersapp/order_form.html'
    success_url = reverse_lazy('order:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreateView, self).get_context_data(**kwargs)
        OrdersFormSet = inlineformset_factory(
            Order,
            OrderItem,
            form=OrderItemForm,
            extra=1,
        )

        if self.request.POST:
            formset = OrdersFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if len(basket_items):
                OrdersFormSet = inlineformset_factory(
                    Order,
                    OrderItem,
                    form=OrderItemForm,
                    extra=len(basket_items),
                )
                formset = OrdersFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity

                basket_items.delete()
            else:
                formset = OrdersFormSet()

        data['order_items'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreateView, self).form_valid(form)


class OrderItemsUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    fields = []
    template_name = 'ordersapp/order_form.html'
    success_url = reverse_lazy('order:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdateView, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order,
            OrderItem,
            form=OrderItemForm,
            extra=1,
        )
        
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, isinstance=self.object)
        else:
            formset = OrderFormSet(isinstance=self.object)
            data['order_items'] = formset
            return data
        
    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']
        
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()
                
        if self.object.get_total_cost() == 0:
            self.object.delete()
            
        return super(OrderItemsUpdateView, self).form_valid(form)


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'ordersapp/order_confirm_delete.html'
    success_url = reverse_lazy('order:orders_list')


class OrderReadView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'ordersapp/order_detail'

    def get_context_data(self, **kwargs):
        context = super(OrderReadView, self).get_context_data(**kwargs)
        context['title'] = 'order/detail view'
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('orders:order_list'))
