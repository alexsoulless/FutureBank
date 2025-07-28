from sqlalchemy import Column, Integer, String, Numeric, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    fio = Column(String(64), nullable=False)
    balance = Column(Numeric(10, 2), default=0.00)
    is_banned = Column(Boolean, default=False)
    role = Column(Integer, default=0)

    transactions_sent = relationship(
        "Transaction", foreign_keys="Transaction.sender_id", back_populates="sender"
    )
    transactions_received = relationship(
        "Transaction",
        foreign_keys="Transaction.recipient_id",
        back_populates="recipient",
    )
    tax_payments = relationship("TaxPayment", back_populates="user")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"))
    transaction_datetime = Column(TIMESTAMP, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

    sender = relationship(
        "User", foreign_keys=[sender_id], back_populates="transactions_sent"
    )
    recipient = relationship(
        "User", foreign_keys=[recipient_id], back_populates="transactions_received"
    )


class Tax(Base):
    __tablename__ = "taxes"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    due_datetime = Column(TIMESTAMP, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

    payments = relationship("TaxPayment", back_populates="tax")


class TaxPayment(Base):
    __tablename__ = "tax_payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tax_id = Column(Integer, ForeignKey("taxes.id"), nullable=False)

    user = relationship("User", back_populates="tax_payments")
    tax = relationship("Tax", back_populates="payments")
