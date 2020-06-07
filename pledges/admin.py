from django.contrib import admin
from pledges.models import Pledge

# Register your models here.


@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):

    search_fields = [
        'first_name', 'last_name', 'description', 'uuid'
    ]

    fields = [
        'first_name',
        'last_name',
        'image',
        'image_ppoi',
        'description',
        'email',
        'confirmed',
        'public',
    ]
