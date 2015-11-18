from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from braces.views import LoginRequiredMixin

from .models import Customer


class CustomerActionMixin(object):
    """Add customized message functionality to create/update actions."""

    fields = ('firstname', 'lastname', 'date_of_birth', 'zip_code')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(CustomerActionMixin, self).form_valid(form)


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer


class CustomerCreateView(LoginRequiredMixin, CustomerActionMixin, CreateView):
    model = Customer
    success_msg = "Customer created."


class CustomerUpdateView(LoginRequiredMixin, CustomerActionMixin, UpdateView):
    model = Customer
    success_msg = "Customer updated."


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('customers:list')


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
