from django.test import TestCase

from gifter.models import User, Wishlist
from django.contrib.auth.models import Group


class TestWishlist(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.users = {
            "mama-bear": User.objects.create_user(
                username="mama-bear",
                email="mama-bear@example.com",
            ),
            "papa-bear": User.objects.create_user(
                username="papa-bear",
                email="papa-bear@example.com",
            ),
            "baby-bear": User.objects.create_user(
                username="baby-bear",
                email="baby-bear@example.com",
            ),
        }
        Group.objects.create(name="The Bears")

    def test_wishlist_creation(self):
        wl1 = Wishlist.objects.create(
            title="Mama's Christmas 2020",
            owner=self.users["mama-bear"],
        )
        wl1.groups.add(Group.objects.get(name="The Bears"))
        wl2 = Wishlist.objects.create(
            title="Papa's Christmas 2020",
            owner=self.users["papa-bear"],
        )
        wl2.groups.add(Group.objects.get(name="The Bears"))
        wl3 = Wishlist.objects.create(
            title="Baby's Christmas 2020",
            owner=self.users["baby-bear"],
        )
        wl3.groups.add(Group.objects.get(name="The Bears"))
        self.assertEqual(Wishlist.objects.count(), 3)
        self.assertEqual(
            Wishlist.objects.filter(owner=self.users["mama-bear"]).count(), 1
        )
        self.assertEqual(
            Wishlist.objects.filter(owner=self.users["papa-bear"]).count(), 1
        )
        self.assertEqual(
            Wishlist.objects.filter(owner=self.users["baby-bear"]).count(), 1
        )
