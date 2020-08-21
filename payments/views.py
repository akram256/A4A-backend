import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from bookings.models import Bookings

# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
def payment_process(request):
    Bookings_id = request.session.get('Bookings_id')
    Bookings = get_object_or_404(Bookings, id=Bookings_id)
    total_cost = Bookings.get_total_cost()
    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the booking as paid
            Bookings.paid = True
            # store the unique transaction id
            Bookings.braintree_id = result.transaction.id
            Bookings.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(request,
                      'payment/process.html',
                      {'Bookings': Bookings,
                       'client_token': client_token})

def payment_done(request):
    return render(request, 'payment/done.html')
def payment_canceled(request):
    return render(request, 'payment/canceled.html')