from django.urls import path
from .views import search_views, Analyze_view

app_name = "search"


urlpatterns = [
    path("", search_views.search, name="search"),
    path("analyze/", Analyze_view.analyze, name="analyze"),
]
