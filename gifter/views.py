from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from gifter.models import Wishlist, Item, Claim


@login_required
def redirect_to_groups(request):
    return redirect(to='group_list')


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'gifter/group_list.html'

    def get_queryset(self):
        return self.request.user.groups.all()


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'gifter/group_detail.html'


class WishlistDetailView(LoginRequiredMixin, DetailView):
    model = Wishlist
    template_name = 'gifter/wishlist_detail.html'

    def get_context_data(self, **kwargs):
        context = super(WishlistDetailView, self).get_context_data(**kwargs)

        me = self.request.user

        context['my_claims'] = Claim.objects.filter(owner=me, item__wishlist=self.object.id)

        return context


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'gifter/item_form.html'
    fields = [
        'title',
        'description',
    ]

    def get_success_url(self):
        return reverse("wishlist_detail", kwargs={
            "pk": str(self.object.wishlist.id)
        })

    def form_valid(self, form):
        user = self.request.user
        wishlist = Wishlist.objects.get(
            id=self.request.resolver_match.kwargs['wishlist_pk']
        )
        if wishlist.owner != self.request.user:
            raise ValidationError("Cannot add items owned by someone other than the wishlist owner")
        form.instance.wishlist_id = str(wishlist.id)
        form.instance.owner = user

        return super(ItemCreateView, self).form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'gifter/item_form.html'
    fields = [
        'title',
        'description',
    ]

    def get_success_url(self):
        return reverse("wishlist_detail", kwargs={
            "pk": str(self.object.wishlist.id)
        })


class ClaimCreateView(LoginRequiredMixin, CreateView):
    model = Claim
    template_name = 'gifter/claim_form.html'
    fields = [
        'description',
    ]

    def get_success_url(self):
        return reverse("wishlist_detail", kwargs={
            "pk": str(self.object.item.wishlist.id)
        })

    def form_valid(self, form):
        user = self.request.user
        item = Item.objects.get(
            id=self.request.resolver_match.kwargs['item_pk']
        )

        form.instance.item = item
        form.instance.owner = user

        return super(ClaimCreateView, self).form_valid(form)


class ClaimUpdateView(LoginRequiredMixin, UpdateView):
    model = Claim
    template_name = 'gifter/claim_form.html'
    fields = [
        'description',
    ]

    def get_success_url(self):
        return reverse("wishlist_detail", kwargs={
            "pk": str(self.object.item.wishlist.id)
        })


class ClaimDeleteView(LoginRequiredMixin, DeleteView):
    model = Claim

    def get_success_url(self):
        return reverse("wishlist_detail", kwargs={
            "pk": str(self.object.item.wishlist.id)
        })