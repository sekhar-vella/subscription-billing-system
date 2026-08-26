from datetime import datetime

from sqlalchemy import Column, Integer, String, Numeric, JSON, DateTime

from app.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    billing_interval = Column(String, nullable=False)
    trial_days = Column(Integer, nullable=False)
    features = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    company_name = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, nullable=False)
    plan_id = Column(Integer, nullable=False)

    status = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
class BillingCycle(Base):
    __tablename__ = "billing_cycles"

    id = Column(Integer, primary_key=True, index=True)

    subscription_id = Column(Integer, nullable=False)

    cycle_start_date = Column(DateTime, nullable=False)
    cycle_end_date = Column(DateTime, nullable=False)
    renewal_date = Column(DateTime, nullable=False)

    status = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    invoice_number = Column(String, nullable=False, unique=True)

    subscription_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)

    invoice_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)

    subtotal = Column(Numeric(10, 2), nullable=False)
    tax_amount = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

    status = Column(String, nullable=False)
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(Integer, nullable=False)

    payment_reference = Column(String, nullable=False, unique=True)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String, nullable=False)

    status = Column(String, nullable=False)
    payment_date = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)

    action = Column(String, nullable=False)

    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)

    performed_by = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)