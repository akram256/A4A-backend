from django.urls import path,include
from rest_framework.routers import DefaultRouter

from Jobs.views import (
                        ArtistCategoryView,ArtistViewSet,
                       ArtistRetrieveUpdateDestroy,
                        UpdateArtistStatus
                        )

# app_name = 'Jobs'
router_v1= DefaultRouter()
router_v1.register('jobs',ArtistViewSet)

urlpatterns = [
    path("artist-categories/", ArtistCategoryView.as_view(), name='job-category'),
    path("artist-categories/<str:id>", ArtistCategoryView.as_view(), name='update-and-delete-category'),
    path('', include(router_v1.urls)),
    path("artist/<str:id>",ArtistRetrieveUpdateDestroy.as_view(),name='update-and-delete-user-job'),
    path("activate_job",UpdateArtistStatus.as_view(), name='activate-inactive-jobs'),
    ]