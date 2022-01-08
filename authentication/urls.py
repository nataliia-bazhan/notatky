from django.urls import path
from . import views

app_name = "auth"

urlpatterns = [
    path("login/", views.log_in, name="log_in"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("log_out/", views.log_out, name="log_out"),
    path("<int:pk>/", views.profile, name="profile"),
    path("change_password/", views.change_password, name='change_password'),
]
