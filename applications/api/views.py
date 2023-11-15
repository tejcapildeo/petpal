from rest_framework import generics
from applications.application import Application
from petlistings.models import PetListing
from .serializers import ApplicationSerializer
from .permissions import IsSeekerOrShelter, IsShelter
from accounts.api.permissions import IsShelterUser


class ApplicationView(generics.RetrieveAPIView):
    permission_classes = [IsSeekerOrShelter]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class ApplicationsViewList(generics.ListAPIView):
    permission_classes = [IsShelterUser]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        pet_listing_id = self.kwargs['pet_listing_id']
        pet_listing = PetListing.objects.filter(id=pet_listing_id)
        return Application.objects.filter(pet_listing=pet_listing)