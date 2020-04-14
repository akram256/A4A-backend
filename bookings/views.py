from django.shortcuts import get_object_or_404
from rest_framework.generics import (UpdateAPIView,
                                     RetrieveUpdateAPIView,
                                     ListAPIView)
from bookings.models import Bookings, Events
from Auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import BookingSerializer,EventSerializer
from rest_framework import status


class BookingArtistView(ListAPIView):
    serializer_class=BookingSerializer
    permission_classes=(IsAuthenticated,)
    queryset=Bookings.objects.all()


    def post(self, request):
        post_data = {"venue":request.data["venue"],"time_of_performance":request.data["time_of_performance"],"conditions":request.data["conditions"],"location":request.data["location"]}
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Booking made"},
                        status=status.HTTP_201_CREATED)

class BookingRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):

    serializer_class=BookingSerializer
    permission_classes=(IsAuthenticated,)
    queryset=Bookings.objects.all()
    lookup_field = 'id'
   

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), id=self.kwargs.get('id'))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message":'Successfully updated'},serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Event has been successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)


class Events(ListAPIView):
    serializer_class=EventSerializer
    permission_classes=(IsAuthenticated,)
    queryset=Events.objects.all()


    def post(self, request):
        post_data = {"artist":request.data["artist"],"date_of_event":request.data["date_of_event"],"venue_of_performance":request.data["venue_of_performance"]}
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Event has been  added"},
                        status=status.HTTP_201_CREATED)


class EventsRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):

    serializer_class=EventSerializer
    permission_classes=(IsAuthenticated,)
    queryset=Events.objects.all()
    lookup_field = 'id'
   

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), id=self.kwargs.get('id'))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message":'Successfully updated'},serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Event has been successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)