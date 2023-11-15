from django.urls import path
from .views import ApplicationView, SeekerApplicationsViewList, ShelterApplicationsViewList, ApplicationCreateView, ApplicationStatusUpdateView

urlpatterns = [ 
    path('seeker/applications/<int:pk>/', ApplicationView.as_view()),
    path('seeker/applications/', SeekerApplicationsViewList.as_view()),
    path('shelter/applications/<int:pk>/', ApplicationView.as_view()),
    path('shelter/applications/', ShelterApplicationsViewList.as_view()),
    path('seeker/applications/create/', ApplicationCreateView.as_view()),
    path('seeker/applications/update/', ApplicationStatusUpdateView.as_view())
]