from rest_framework import generics, status
from rest_framework.response import Response
from applications.application import Application
from accounts.models import Seeker, Shelter
# from petlistings.models import PetListing
from .serializers import ApplicationSerializer, ApplicationStatusUpdateSerializer
from .permissions import HasApplicationPermission
from accounts.api.permissions import IsShelterUser, IsSeekerUser


class ApplicationView(generics.RetrieveAPIView):
    permission_classes = [IsShelterUser|IsSeekerUser, HasApplicationPermission]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class ApplicationCreateView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pet_listing_id = serializer.validated_data.get('pet_listing').id
        # pet_listing = PetListing.objects.get(id=pet_listing_id)

        # TODO: RETURN ONCE CHANGES ARE MADE TO PETLISTING
        # if pet_listing.status != PetListing.status.AVAILABLE:
        #     return Response({"error": "This pet is not available for adoption."}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ApplicationStatusUpdateView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationStatusUpdateSerializer

    def update(self, request, *args, **kwargs):
        application = self.get_object()
        current_user = request.user
        new_status = request.data.get('status')

        if application.pet_seeker.user == current_user:
            if application.status != Application.Status.PENDING and application.status != Application.Status.ACCEPTED:
                return Response({"error": "You can only withdraw a pending or accepted application."}, status=status.HTTP_400_BAD_REQUEST)
            if new_status != Application.Status.WITHDRAWN:
                return Response({"error": "You can only change status to withdrawn."}, status=status.HTTP_400_BAD_REQUEST)

        elif application.shelter.user == current_user:
            if application.status != Application.Status.PENDING:
                return Response({"error": "You can only accept or deny a pending application."}, status=status.HTTP_400_BAD_REQUEST)
            if new_status not in [Application.Status.ACCEPTED, Application.Status.DENIED]:
                return Response({"error": "Invalid status update."}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"error": "You do not have permission to update this application."}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)


class ShelterApplicationsViewList(generics.ListAPIView):
    permission_classes = [IsShelterUser]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        shelter = Shelter.objects.get(user=user)
        applications = Application.objects.filter(shelter=shelter)

        status = self.request.query_params.get('status', None)
        if status is not None:
            applications = applications.filter(status=status)

        ordering = self.request.query_params.get('ordering')
        if ordering:
            applications = applications.order_by(ordering)

        return applications
    

class SeekerApplicationsViewList(generics.ListAPIView):
    permission_classes = [IsSeekerUser]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        seeker = Seeker.objects.get(user=user)
        applications = Application.objects.filter(pet_seeker=seeker)

        status = self.request.query_params.get('status', None)
        if status is not None:
            applications = applications.filter(status=status)

        ordering = self.request.query_params.get('ordering')
        if ordering:
            applications = applications.order_by(ordering)

        return applications