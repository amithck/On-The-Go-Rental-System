from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, Optional


class PaymentGatewayError(Exception):
    """Base exception for payment gateway failures."""


class PaymentDeclinedError(PaymentGatewayError):
    """Raised when the gateway declines a charge."""


class PaymentConfigurationError(PaymentGatewayError):
    """Raised when the gateway is not configured correctly."""


@dataclass
class GatewayResponse:
    success: bool
    transaction_id: Optional[str] = None
    message: Optional[str] = None
    data: Dict[str, Any] = None


class GenericPaymentGatewayAdapter:
    """Generic payment gateway adapter stub for future provider integration."""

    def charge(self, amount: Decimal, currency: str, metadata: Optional[Dict[str, Any]] = None) -> GatewayResponse:
        if amount <= 0:
            raise PaymentGatewayError('Charge amount must be positive.')

        return GatewayResponse(
            success=True,
            transaction_id='GATEWAY-STUB-0001',
            message='Charge authorized successfully',
            data={'amount': str(amount), 'currency': currency, 'metadata': metadata or {}}
        )

    def top_up(self, amount: Decimal, currency: str, card_number: str) -> GatewayResponse:
        if amount <= 0:
            raise PaymentGatewayError('Top-up amount must be positive.')
        if not card_number.isdigit() or len(card_number) not in (12, 13, 14, 15, 16):
            raise PaymentGatewayError('Invalid card number format.')

        return GatewayResponse(
            success=True,
            transaction_id='GATEWAY-STUB-0002',
            message='Card charged successfully',
            data={'amount': str(amount), 'currency': currency, 'card_last4': card_number[-4:]}
        )
