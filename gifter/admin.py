from django.contrib import admin

from gifter.models import User, Wishlist, Item, Claim

admin.site.register(User)
admin.site.register(Wishlist)
admin.site.register(Item)
admin.site.register(Claim)
