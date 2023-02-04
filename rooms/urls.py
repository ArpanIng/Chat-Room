from django.urls import path
from . import views

app_name = "rooms"
urlpatterns = [
    path("", views.homepage_view, name="homepage"),
    path("topics/", views.topics_view, name="topics"),
    path("activities/", views.activities_view, name="activities"),
    path("room/<int:pk>/", views.room_detail_view, name="room_detail"),
    path("room/add/", views.room_create_view, name="room_create"),
    path("room/<int:pk>/edit/", views.room_update_view, name="room_update"),
    path("room/<int:pk>/delete/", views.room_delete_view, name="room_delete"),
    path("message/<int:pk>/delete/", views.message_delete_view, name="message_delete"),
]
