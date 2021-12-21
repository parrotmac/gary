from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from gifter.views import GroupListView, GroupDetailView, redirect_to_groups, WishlistDetailView, ItemCreateView, \
    ItemUpdateView, ClaimCreateView, ClaimUpdateView, ClaimDeleteView

urlpatterns = [
    path('', redirect_to_groups, name='redirect_to_groups'),
    path('groups', GroupListView.as_view(), name='group_list'),
    path('groups/<str:pk>', GroupDetailView.as_view(), name='group_detail'),
    path('wishlists/<str:pk>', WishlistDetailView.as_view(), name='wishlist_detail'),
    path('wishlists/<str:wishlist_pk>/items/create', ItemCreateView.as_view(), name='item_create'),
    path('wishlists/<str:wishlist_pk>/items/<str:pk>', ItemUpdateView.as_view(), name='item_update'),
    path('wishlists/<str:wishlist_pk>/items/<str:item_pk>/claims/create', ClaimCreateView.as_view(), name='claim_create'),
    path('wishlists/<str:wishlist_pk>/items/<str:item_pk>/claims/<str:pk>', ClaimUpdateView.as_view(), name='claim_update'),
    path('wishlists/<str:wishlist_pk>/items/<str:item_pk>/claims/<str:pk>/delete', ClaimDeleteView.as_view(), name='claim_delete'),
    path('accounts/profile/', TemplateView.as_view(template_name='accounts/profile.html')),
]
