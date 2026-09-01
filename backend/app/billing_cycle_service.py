from datetime import datetime
from calendar import monthrange

from sqlalchemy.orm import Session

from app import models


def add_months(date: datetime, months: int) -> datetime:
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1

    day = min(
        date.day,
        monthrange(year, month)[1]
    )

    return date.replace(
        year=year,
        month=month,
        day=day
    )


def calculate_next_renewal_date(
    start_date: datetime,
    billing_interval: str
) -> datetime:

    if billing_interval.lower() == "monthly":
        return add_months(start_date, 1)

    if billing_interval.lower() == "annual":
        return add_months(start_date, 12)

    raise ValueError(
        f"Unsupported billing interval: {billing_interval}"
    )


def create_billing_cycle(
    subscription_id: int,
    db: Session
):
    subscription = (
        db.query(models.Subscription)
        .filter(models.Subscription.id == subscription_id)
        .first()
    )

    if subscription is None:
        raise ValueError("Subscription not found")

    plan = (
        db.query(models.Plan)
        .filter(models.Plan.id == subscription.plan_id)
        .first()
    )

    if plan is None:
        raise ValueError("Plan not found")

    cycle_start_date = subscription.start_date

    renewal_date = calculate_next_renewal_date(
        cycle_start_date,
        plan.billing_interval
    )

    cycle_end_date = renewal_date

    billing_cycle = models.BillingCycle(
        subscription_id=subscription.id,
        cycle_start_date=cycle_start_date,
        cycle_end_date=cycle_end_date,
        renewal_date=renewal_date,
        status="scheduled"
    )

    db.add(billing_cycle)
    db.commit()
    db.refresh(billing_cycle)

    return billing_cycle