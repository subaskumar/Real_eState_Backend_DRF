from django.urls import path
from .views import ListingsView, ListingView, SearchView,AddListingView

urlpatterns = [
    path('', ListingsView.as_view()),
    path('search/', SearchView.as_view()),
    path('<slug>', ListingView.as_view()),
    path('add_listing/',AddListingView.as_view()),
    # path('<int:pk>', ListingView.as_view()),

]
