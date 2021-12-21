from django.urls import path

from gifter.views import GroupListView, GroupDetailView, redirect_to_groups, WishlistDetailView, ItemCreateView, \
    ItemUpdateView, ClaimCreateView, ClaimUpdateView, ClaimDeleteView, accept_invitation, incoming_invitation, \
    ProfileView, health_check

urlpatterns = [
    path('healthz', health_check, name='health_check'),
    path('', redirect_to_groups, name='redirect_to_groups'),
    path('groups', GroupListView.as_view(), name='group_list'),
    path('groups/<str:pk>', GroupDetailView.as_view(), name='group_detail'),
    path('wishlists/<str:pk>', WishlistDetailView.as_view(), name='wishlist_detail'),
    path('wishlists/<str:wishlist_pk>/items/create', ItemCreateView.as_view(), name='item_create'),
    path('wishlists/<str:wishlist_pk>/items/<str:pk>', ItemUpdateView.as_view(), name='item_update'),
    path('wishlists/<str:wishlist_pk>/items/<str:item_pk>/claims/create', ClaimCreateView.as_view(), name='claim_create'),
    path('wishlists/<str:wishlist_pk>/items/<str:item_pk>/claims/<str:pk>', ClaimUpdateView.as_view(), name='claim_update'),
    path('wishlists/<str:wishlist_pk>/items/<str:item_pk>/claims/<str:pk>/delete', ClaimDeleteView.as_view(), name='claim_delete'),
    path('invitations/incoming/<str:token>', incoming_invitation, name='accept_invitation'),
    path('invitations/accept', accept_invitation, name='accept_invitation'),
    path('accounts/profile', ProfileView.as_view(), name='profile_view'),
]
