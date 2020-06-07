from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from django.db import models
import secrets
import uuid
from imagefield.fields import ImageField

# Create your models here.


class Pledge(models.Model):
    first_name = models.CharField(
        _('first name'), max_length=40
    )

    last_name = models.CharField(
        _('last name'),
        max_length=40,
    )

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)

    image = ImageField(
        _("image"),
        formats={
            'large': ['default', ('crop', (760, 760))],
            'preview': ['default', ('crop', (1200, 630))],
        }, blank=True, auto_add_fields=True
    )

    description = models.CharField(
        _("description"),
        max_length=140, blank=True
    )

    email = models.EmailField(_("e-mail"), unique=True)

    token = models.CharField(
        max_length=60, default=secrets.token_urlsafe,
        blank=True,
    )

    confirmed = models.BooleanField(default=False)

    confirmed_at = models.DateField(blank=True, null=True)

    public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('pledge_list') + f"?featured={self.pk}"

    class Meta:
        ordering = ['-created_at']

