from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path("", views.all_notes, name="notes"),
    path("user_notes/", views.user_notes, name="user_notes"),
    path('create_note/', views.create_note, name='create_note'),
    path('update_note/', views.update_note, name='update_note'),
    path('delete_note/', views.delete_note, name='delete_note'),
    path("note/<int:pk>", views.details_note, name="details_note"),
]
