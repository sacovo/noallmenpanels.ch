from django.urls import path
from pledges import views

app_name = 'pledges'

urlpatterns = [
    path('', views.pledge_list, name="pledge_list"),
    path('create/', views.create_pledge, name="create_pledge"),
    path('confirm/<uuid:uuid>/<token>/',
         views.confirm_pledge, name="confirm_pledge")
]
