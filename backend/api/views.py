from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .filters import CatFilter
from .models import Breed, Cat, Rating
from .permissions import IsOwner
from .serializers import BreedSerializer, CatSerializer, RatingSerializer


class BreedListView(generics.ListAPIView):
    queryset = Breed.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = BreedSerializer


class CatViewSet(ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CatFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(who_rates=self.request.user)
