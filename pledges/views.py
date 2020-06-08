from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from pledges.models import Pledge
from pledges.forms import PledgeForm

# Create your views here.


def pledge_list(request):
    pledges = Pledge.objects.filter(
            public=True, confirmed=True
    )

    if query := request.GET.get('q'):
        pledges = pledges.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(description__icontains=query)
        )

    page = Paginator(pledges, 24).page(
        int(request.GET.get('page', '1'))
    )

    meta = {
        'title': _('#NoAllMalePanels'),
        'image': '/static/preview.png',
    }

    featured = None

    if featured := request.GET.get('featured', ''):
        featured = Pledge.objects.get(pk=featured)
        meta.update({
            'title': _(f"#NoAllMalePanels - {featured.first_name} {featured.last_name}"),
            'image': featured.image.preview
        })

    return render(request, 'pledges/pledge_list.html', {
        'page': page,
        'query': query,
        'meta': meta,
        'featured': featured,
    })


def create_pledge(request):
    form = PledgeForm(label_suffix='')

    if request.method == 'POST':
        form = PledgeForm(request.POST, request.FILES, label_suffix='')

        if form.is_valid():
            pledge = form.save()

            send_mail(
                _('#NoAllMenPanels-Challenge Bestätigung'),
                _(f"""Hallo {pledge.first_name} {pledge.last_name}
Bestätige deine ... unter
https://{request.get_host()}/confirm/{pledge.uuid}/{pledge.token}/

Vielen Dank und freundliche Grüsse
"""
                 ),
                'allmalepanels@sandrocovo.ch',
                [pledge.email],
            )
            return render(request, 'pledges/success.html', {
                'form': form,
                'pledge': pledge,
            })

    return render(request, 'pledges/create_pledge.html', {
        'form': form,
    })


def confirm_pledge(request, token, uuid):
    pledge = get_object_or_404(Pledge, uuid=uuid)

    if not pledge.confirmed and pledge.token == token:
        pledge.confirmed=True
        pledge.confirmed_at = timezone.now()
        pledge.save()
        return render(request, 'pledges/confirm_success.html', {
            'pledge': pledge
        })

    return render(request, 'pledges/confirm_error.html', {
        'pledge': pledge
    })
