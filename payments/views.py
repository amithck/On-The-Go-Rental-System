from decimal import Decimal, InvalidOperation
from datetime import datetime
import random
import string

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F

from .models import payments_bike, payments_user
from .gateway import GenericPaymentGatewayAdapter, PaymentGatewayError
from bike_and_terminal.models import bike as Bike, terminal as Terminal
from user.models import auth as UserProfile

payment_gateway = GenericPaymentGatewayAdapter()


@login_required(login_url='/signin')
def payment(request):
    if request.method != 'POST':
        return redirect('show_loc')

    bike_id = request.POST.get('bike_chosen', '').strip()
    current_user = request.user
    user_profile = UserProfile.objects.filter(email=str(current_user)).first()
    rent_quotes = request.session.get('rent_quotes', {})
    selected_quote = rent_quotes.get(bike_id)

    if not bike_id or not user_profile or not selected_quote:
        return render(request, 'payment.html', {
            'error': 'Unable to complete payment. Missing rent quote or user profile.',
            'query_results': [],
            'dis': None,
        })

    try:
        rent_amount = Decimal(str(selected_quote.get('rent_cost', '0')))
    except (InvalidOperation, TypeError):
        return render(request, 'payment.html', {
            'error': 'Invalid rent quote amount provided.',
            'query_results': [],
            'dis': None,
        })

    if rent_amount <= 0:
        return render(request, 'payment.html', {
            'error': 'Rent amount must be positive.',
            'query_results': [],
            'dis': None,
        })

    if user_profile.balance < rent_amount:
        return render(request, 'payment.html', {
            'error': 'Insufficient balance for this rental.',
            'query_results': [],
            'dis': rent_amount,
        })

    receipt_no = None
    try:
        with transaction.atomic():
            bike_obj = Bike.objects.select_for_update().get(pk=bike_id)
            from_terminal = Terminal.objects.select_for_update().get(term_id=selected_quote.get('fromt'))
            to_terminal = Terminal.objects.select_for_update().get(term_id=selected_quote.get('tot'))

            gateway_response = payment_gateway.charge(
                amount=rent_amount,
                currency='INR',
                metadata={'bike_id': bike_id, 'user': str(current_user)},
            )
            if not gateway_response.success:
                raise PaymentGatewayError(gateway_response.message or 'Payment gateway declined the charge.')

            bike_obj.term_id = to_terminal
            bike_obj.save(update_fields=['term_id'])

            from_terminal.no_of_bikes = F('no_of_bikes') - 1
            from_terminal.save(update_fields=['no_of_bikes'])
            to_terminal.no_of_bikes = F('no_of_bikes') + 1
            to_terminal.save(update_fields=['no_of_bikes'])

            user_profile.balance = F('balance') - rent_amount
            user_profile.save(update_fields=['balance'])
            user_profile.refresh_from_db()

            receipt_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            payments_bike.objects.create(
                receipt_no=receipt_no,
                bike_id=bike_obj,
                email=user_profile,
                cost=str(rent_amount),
            )
    except (Bike.DoesNotExist, Terminal.DoesNotExist, PaymentGatewayError) as exc:
        return render(request, 'payment.html', {
            'error': str(exc),
            'query_results': [],
            'dis': rent_amount,
        })

    query_results = [
        receipt_no,
        datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
        bike_id,
        str(current_user),
        str(rent_amount),
    ]
    return render(request, 'payment.html', {
        'query_results': query_results,
        'dis': rent_amount,
    })


@login_required(login_url='/signin')
def update_balance(request):
    current_user = request.user
    user_profile = UserProfile.objects.filter(email=str(current_user)).first()
    balance = user_profile.balance if user_profile else 0
    text = f"Current balance: {balance}"
    return render(request, 'update_balance.html', {'text': text})


@login_required(login_url='/signin')
def update_balance_receipt(request):
    current_user = request.user
    user_profile = UserProfile.objects.filter(email=str(current_user)).first()
    context = {}

    if request.method == 'POST':
        add_balance_value = request.POST.get('balance', '').strip()
        credit = request.POST.get('card', '').strip()

        try:
            add_balance = Decimal(add_balance_value)
        except (InvalidOperation, TypeError):
            context['error'] = 'Please enter a valid amount.'
            return render(request, 'update_balance_receipt.html', context)

        if add_balance <= 0:
            context['error'] = 'Top-up amount must be greater than zero.'
            return render(request, 'update_balance_receipt.html', context)

        if not user_profile:
            context['error'] = 'User profile not found.'
            return render(request, 'update_balance_receipt.html', context)

        try:
            gateway_response = payment_gateway.top_up(
                amount=add_balance,
                currency='INR',
                card_number=credit,
            )
            if not gateway_response.success:
                raise PaymentGatewayError(gateway_response.message or 'Card top-up failed.')

            with transaction.atomic():
                user_profile.balance = F('balance') + add_balance
                user_profile.save(update_fields=['balance'])
                user_profile.refresh_from_db()

                receipt_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                payments_user.objects.create(
                    receipt_no=receipt_no,
                    email=user_profile,
                    cost=str(add_balance),
                    cardNo=credit,
                )

            context['query_results'] = [
                receipt_no,
                datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
                str(current_user),
                str(add_balance),
                credit,
            ]
            context['text'] = f"Current balance: {user_profile.balance}"
        except PaymentGatewayError as exc:
            context['error'] = str(exc)

    return render(request, 'update_balance_receipt.html', context)


@login_required(login_url='/signin')
def show_transactions(request):
    current_user = request.user
    user_pay = payments_user.objects.filter(email=str(current_user))
    bike_pay = payments_bike.objects.filter(email=str(current_user))
    context = {'user_pay': user_pay, 'bike_pay': bike_pay}
    return render(request, 'show_transactions.html', context)
