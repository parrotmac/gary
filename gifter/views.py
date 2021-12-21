import re
from datetime import datetime

from allauth.account.views import LogoutView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.defaultfilters import pluralize
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from gifter.models import Wishlist, Item, Claim, GroupInvitation


# https://djangosnippets.org/snippets/2926/
def possessive(value):
    """
    Add an "'s" or "'" where appropriate on proper nouns to to make them posessive
    """
    if re.search(r's$', value):
        return value + "'"
    else:
        return value + "'s"


@login_required
def redirect_to_groups(request):
    return redirect(to='group_list')


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'gifter/group_form.html'
    fields = [
        'name',
    ]

    def get_success_url(self):
        return reverse("group_detail", kwargs={
            "pk": str(self.object.id)
        })

    def form_valid(self, form):
        user = self.request.user
        form.instance.save()
        form.instance.user_set.add(user)
        return super(GroupCreateView, self).form_valid(form)

    def get_initial(self):
        try:
            social_family = self.request.user.socialaccount_set.first().extra_data.get('family_name')
            if social_family:
                return {
                    'name': f"{social_family} Family Christmas - {datetime.now().year}"
                }
        except Exception:
            pass
        return {}


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = 'gifter/group_form.html'
    fields = [
        'name',
    ]

    def get_success_url(self):
        return reverse("group_detail", kwargs={
            "pk": str(self.object.id)
        })


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'gifter/group_list.html'

    def get_queryset(self):
        return self.request.user.groups.all()


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'gifter/group_detail.html'


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = "gifter/group_confirm_delete.html"

    def get_success_url(self):
        return reverse("group_list")


class WishlistDetailView(LoginRequiredMixin, DetailView):
    model = Wishlist
    template_name = 'gifter/wishlist_detail.html'

    def get_context_data(self, **kwargs):
        context = super(WishlistDetailView, self).get_context_data(**kwargs)

        me = self.request.user

        context['my_claims'] = Claim.objects.filter(owner=me, item__wishlist=self.object.id)

        return context


class WishlistCreateView(LoginRequiredMixin, CreateView):
    model = Wishlist
    template_name = 'gifter/wishlist_form.html'
    fields = [
        'title',
    ]

    def get_initial(self):
        name = "My"
        try:
            social_given = self.request.user.socialaccount_set.first().extra_data.get('given_name')
            if social_given:
                name = social_given
        except Exception:
            if self.request.user.first_name:
                name = self.request.user.first_name

        return {
            'title': f"{possessive(name)} Wishlist",
        }

    def get_success_url(self):
        return reverse("wishlist_detail", kwargs={
            "group_pk": str(self.object.group.id),
            "pk": str(self.object.id)
        })

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        form.instance.group_id = self.request.resolver_match.kwargs['group_pk']
        return super(WishlistCreateView, self).form_valid(form)


class WishlistUpdateView(LoginRequiredMixin, UpdateView):
    model = Wishlist
    template_name = 'gifter/wishlist_form.html'
    fields = [
        'title',
    ]

    def get_success_url(self):
        return reverse("wishlist_detail", kwargs={
            "group_pk": str(self.object.group.id),
            "pk": str(self.object.id)
        })


class WishlistDeleteView(LoginRequiredMixin, DeleteView):
    model = Wishlist
    template_name = "gifter/wishlist_confirm_delete.html"

    def get_success_url(self):
        return reverse("group_detail", kwargs={
            "pk": self.object.group.id,
        })


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'gifter/item_form.html'
    fields = [
        'title',
        'description',
    ]

    def get_success_url(self):
        return reverse("wishlist_detail", kwargs={
            "pk": str(self.object.wishlist.id),
            "group_pk": self.object.wishlist.group_id,
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


def incoming_invitation(request, token):
    """
    incoming_invitation stores the incoming token in the session to be retrieved later
    """
    request.session['invitation_token'] = token
    return redirect(to='accept_invitation')


@login_required
def accept_invitation(request):
    """
    after being stored by invitation_token, accept_invitation pulls the stored
    token off of the session and adds the user to the pre-determined group
    """
    next_view = request.GET.get('next', reverse('group_list'))
    stored_token = request.session.pop("invitation_token", None)
    if not stored_token:
        messages.add_message(
            request,
            level=messages.WARNING,
            message="There was an issue accepting an invitation. Perhaps the invitation was already accepted?",
            fail_silently=True,
        )
        return redirect(to=next_view)
    try:
        invitation = GroupInvitation.objects.get(verification_code=stored_token, destination_email=request.user.email)
        if not invitation.verified_at:
            request.user.groups.add(invitation.target_group)
            invitation.verified_at = timezone.now()
            invitation.save()
        return redirect(to=reverse('group_detail', kwargs={
            'pk': invitation.target_group_id,
        }))
    except GroupInvitation.DoesNotExist:
        messages.add_message(
            request,
            level=messages.WARNING,
            message="There was an issue accepting an invitation. Perhaps the invitation was already accepted?",
            fail_silently=True,
        )
    return redirect(to=next_view)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        if 'invitation_token' in request.session.keys():
            return redirect(to=f"{reverse('accept_invitation')}?next={reverse('profile_view')}")
        return super(ProfileView, self).get(self, request, *args, **kwargs)


class ProfileLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'account/logout.html'


def health_check(request):
    return HttpResponse("OK")
