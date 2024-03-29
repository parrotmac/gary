# Generated by Django 4.0 on 2021-12-21 06:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import gifter.models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("gifter", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GroupInvitation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("destination_email", models.EmailField(max_length=254)),
                (
                    "verification_code",
                    models.CharField(
                        default=gifter.models.verification_code,
                        editable=False,
                        max_length=16,
                    ),
                ),
                ("sent_at", models.DateTimeField(blank=True, null=True)),
                ("verified_at", models.DateTimeField(blank=True, null=True)),
                (
                    "resulting_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="accepted_invitations",
                        to="gifter.user",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="send_invitations",
                        to="gifter.user",
                    ),
                ),
                (
                    "target_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="auth.group"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
