from django.urls import path

from gifter.views import GroupListView, GroupDetailView, redirect_to_groups, WishlistDetailView, ItemCreateView, \
    ItemUpdateView, ClaimCreateView, ClaimUpdateView, ClaimDeleteView, accept_invitation, incoming_invitation, \
    ProfileView, health_check, GroupCreateView, GroupUpdateView, WishlistCreateView, WishlistUpdateView, \
    WishlistDeleteView, GroupDeleteView, SendInviteFormView

urlpatterns = [
    path('healthz', health_check, name='health_check'),
    path('', redirect_to_groups, name='redirect_to_groups'),
    path('groups', GroupListView.as_view(), name='group_list'),
    path('groups/create', GroupCreateView.as_view(), name='group_create'),
    path('groups/<str:pk>', GroupDetailView.as_view(), name='group_detail'),
    path('groups/<str:pk>/delete', GroupDeleteView.as_view(), name='group_delete'),
    path('groups/<str:pk>/update', GroupUpdateView.as_view(), name='group_update'),
    path('groups/<str:group_pk>/wishlists/create', WishlistCreateView.as_view(), name='wishlist_create'),
    path('groups/<str:group_pk>/wishlists/<str:pk>', WishlistDetailView.as_view(), name='wishlist_detail'),
    path('groups/<str:group_pk>/wishlists/<str:pk>/update', WishlistUpdateView.as_view(), name='wishlist_update'),
    path('groups/<str:group_pk>/wishlists/<str:pk>/delete', WishlistDeleteView.as_view(), name='wishlist_delete'),
    path('wishlists/<str:wishlist_pk>/items/create', ItemCreateView.as_view(), name='item_create'),
    path('wishlists/<str:wishlist_pk>/items/<str:pk>', ItemUpdateView.as_view(), name='item_update'),
    path('wishlists/<str:wishlist_pk>/items/<str:item_pk>/claims/create', ClaimCreateView.as_view(), name='claim_create'),
    path('wishlists/<str:wishlist_pk>/items/<str:item_pk>/claims/<str:pk>', ClaimUpdateView.as_view(), name='claim_update'),
    path('wishlists/<str:wishlist_pk>/items/<str:item_pk>/claims/<str:pk>/delete', ClaimDeleteView.as_view(), name='claim_delete'),
    path('invitations/incoming/<str:token>', incoming_invitation, name='accept_invitation'),
    path('invitations/accept', accept_invitation, name='accept_invitation'),
    path('groups/<str:group_pk>/invitations/send', SendInviteFormView.as_view(), name='send_invite'),
    path('accounts/profile', ProfileView.as_view(), name='profile_view'),
]
