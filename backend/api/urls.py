from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BreedListView, CatViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'cats', CatViewSet, basename='cat')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
    path('breeds/', BreedListView.as_view(), name='breeds'),
]
