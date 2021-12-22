import hashlib
import uuid
import secrets

from django.contrib.auth.models import Group, AbstractUser
from django.db import models
from django.utils import timezone


class CommonBaseClass(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)
    deleted_at = models.DateTimeField(blank=True, null=True, editable=True)

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(CommonBaseClass, self).save(*args, **kwargs)

    def __str__(self):
        str_data = []
        if self.id:
            str_data.append(str(self.id))
        if hasattr(self, "uuid"):
            str_data.append(str(self.uuid))
        if hasattr(self, "name"):
            str_data.append(self.name)
        return " / ".join(str_data)


class User(AbstractUser, CommonBaseClass):
    nickname = models.CharField(max_length=30, blank=True, null=True)

    @property
    def display_photo(self):
        if self.socialaccount_set.count() > 0:
            social_image = self.socialaccount_set.first().extra_data.get('picture')
            return social_image
        if self.email:
            return f'https://www.gravatar.com/avatar/{hashlib.md5(self.email.encode("utf-8")).hexdigest()}?d=retro'
        # Return a 'mystery person' if nothing else is available
        return 'https://www.gravatar.com/avatar/5f4dcc3b5aa765d61d8327deb882cf99?d=mp'

    @property
    def display_name(self):
        if self.socialaccount_set.count() > 0:
            if social_account_name := self.socialaccount_set.first().extra_data.get('name'):
                return social_account_name
        if self.first_name:
            return self.first_name
        if self.email:
            return self.email
        return self.username

    @property
    def display_email(self):
        if self.email:
            return self.email
        if self.socialaccount_set.count() > 0:
            if social_account_email := self.socialaccount_set.first().extra_data.get('email'):
                return social_account_email
        return None

    def __str__(self):
        return self.display_name


class Wishlist(CommonBaseClass):
    title = models.CharField(max_length=120, blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"Wishlist for {self.owner} on {self.group.name}"


class Item(CommonBaseClass):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Item details
    title = models.CharField(max_length=120, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    links = models.JSONField(default=list, blank=True, null=True)
    # TODO: Add support for photos

    def __str__(self):
        return f"{self.owner} - {self.title}"


class Claim(CommonBaseClass):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Details of claim
    description = models.TextField(blank=True, null=True)
    links = models.JSONField(default=list, blank=True, null=True)
    # TODO: Add support for photos

    def __str__(self):
        return f"{self.owner} claims {self.item}"


def verification_code():
    return secrets.token_urlsafe(16)


class GroupInvitation(CommonBaseClass):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, null=False, related_name='send_invitations')
    target_group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, blank=False, null=False)
    destination_email = models.EmailField(blank=False, null=False)
    verification_code = models.CharField(max_length=32, editable=False, null=False, blank=False, default=verification_code)
    sent_at = models.DateTimeField(blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    resulting_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='accepted_invitations')
    http_origin = models.URLField(blank=True, null=True)  # Used when constructing invitation URL
