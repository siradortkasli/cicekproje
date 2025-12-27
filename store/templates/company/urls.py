from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.company_login, name="company_login"),
    path("dashboard/", views.company_dashboard, name="company_dashboard"),
]
