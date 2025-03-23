from enum import Enum


class InvoiceStatus(Enum):
    wait = 'WAIT'
    expired = 'EXPIRED'
    complete = 'COMPLETE'
    under_paid = 'UNDER_PAID'
    over_paid = 'OVER_PAID'