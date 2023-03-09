import datetime
import logging
from urllib.parse import urlparse

from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from gary.settings import (
    SENDGRID_ENABLED,
    SENDGRID_EMAIL_INVITE_TEMPLATE,
    INVITE_EMAIL_COOLDOWN_PERIOD_MINUTES,
    DEFAULT_FROM_EMAIL,
)
from gifter.models import GroupInvitation

logger = logging.getLogger(__name__)


@receiver(post_save, sender=GroupInvitation, dispatch_uid="group_invitation_created")
def invitation_saved(sender, instance: GroupInvitation, created: bool, **kwargs):
    if created and not instance.sent_at:

        most_recent_matching_invitations = GroupInvitation.objects.filter(
            sender=instance.sender,
            destination_email=instance.destination_email,
            target_group=instance.target_group,
            verified_at=None,
            sent_at__isnull=False,
        ).order_by("-created_at")
        if most_recent_matching_invitations.count() > 0:
            if most_recent_matching_invitations.first().sent_at > (
                timezone.now()
                - datetime.timedelta(minutes=int(INVITE_EMAIL_COOLDOWN_PERIOD_MINUTES))
            ):
                logger.info(
                    f"Skipping send of invitation to {instance.destination_email} as there's an outstanding email within the last 5 minutes"
                )
                return

        if SENDGRID_ENABLED:
            from_email = DEFAULT_FROM_EMAIL
            http_origin_url = (
                urlparse(instance.http_origin)
                if instance.http_origin
                else urlparse("https://wishlist.parker.style")
            )

            port_spec = ""
            if http_origin_url.port:
                if http_origin_url.scheme == "http" and http_origin_url.port == "80":
                    pass
                elif (
                    http_origin_url.scheme == "https" and http_origin_url.port == "443"
                ):
                    pass
                else:
                    port_spec = f":{http_origin_url.port}"
            path = reverse(
                "accept_invitation", kwargs={"token": instance.verification_code}
            )

            try:
                msg = EmailMessage(
                    from_email=from_email,
                    reply_to=["isaac@sianware.com"],
                    to=[instance.destination_email],
                )
                msg.template_id = SENDGRID_EMAIL_INVITE_TEMPLATE

                msg.dynamic_template_data = {
                    "invited_by": instance.sender.display_name,
                    "verification_url": f"{http_origin_url.scheme}://{http_origin_url.hostname}{port_spec}{path}",
                }
                msg.send(
                    fail_silently=True
                )  # FIXME: This is reporting errors even when successful!

                instance.sent_at = timezone.now()
                instance.save()
            except Exception as e:
                logger.error(
                    f"Failed to send email to {instance.destination_email} from {from_email}",
                    e,
                )
