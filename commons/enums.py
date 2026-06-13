from enum import Enum

class SubscriptionEvent(str, Enum):
    ACTIVE = "subscription.active"
    CANCELLED = "subscription.cancelled"
    EXPIRED = "subscription.expired"
    FAILED = "subscription.failed"
    ON_HOLD = "subscription.on_hold"
    PLAN_CHANGED = "subscription.plan_changed"
    RENEWED = "subscription.renewed"
    UPDATED = "subscription.updated"

class PaymentEvent(str, Enum):
    CANCELLED = "payment.cancelled"
    FAILED = "payment.failed"
    PROCESSING = "payment.processing"
    SUCCEEDED = "payment.succeeded"