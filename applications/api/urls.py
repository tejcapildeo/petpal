from django.urls import path
from .views import ApplicationView, ApplicationsViewList

urlpatterns = [ 
    path('seeker/applications/<int:pk>', ApplicationView.as_view()),
    path('seeker/applications/', ApplicationsViewList.as_view())
]