from django.urls import path,include

from tickets.views import (
                        TicketView
                        )

app_name = 'tickets'


urlpatterns = [
    path("tickets", TicketView.as_view(), name='tickets'),

]