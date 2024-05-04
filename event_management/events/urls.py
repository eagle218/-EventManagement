from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventRegistrationViewSet
from django.urls import include, path

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'eventregistrations', EventRegistrationViewSet)

urlpatterns = [
    path('', views.EventList.as_view(), name='event-list'),
    path('users/', views.UserCreate.as_view(), name='user-create'),
    path('<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
    path('create/', views.EventCreate.as_view(), name='event-create'),
    path('update/<int:pk>/', views.EventUpdate.as_view(), name='event-update'),
    path('delete/<int:pk>/', views.EventDelete.as_view(), name='event-delete'),
    path('', include(router.urls)),

]


