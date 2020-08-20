from django.shortcuts import render
from rest_framework.generics import (UpdateAPIView,
                                     RetrieveUpdateAPIView,
                                     ListAPIView,RetrieveUpdateDestroyAPIView)
from Auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status

from .serializers import TicketSerializer
from .models import Tickets

# Create your views here.

class TicketView(ListAPIView):
    serializer_class = TicketSerializer
    permissions_class= (AllowAny,)
    queryset= Tickets.objects.all()


class UpdateNoofTickets(RetrieveUpdateDestroyAPIView):
    permission_classes =(AllowAny,)
    serializer_class = TicketSerializer
    lookup_field = 'id'
    queryset= Tickets.objects.all()

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
        return Response({'message':'successfully Updated',
        'data':serializer.data},status=status.HTTP_200_OK)