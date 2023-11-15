from django.urls import path
from .views import ApplicationView, ApplicationsViewList, ApplicationCreateView

urlpatterns = [ 
    path('applications/<int:pk>/', ApplicationView.as_view(), name="application"),
    path('applications/', ApplicationsViewList.as_view()),
]