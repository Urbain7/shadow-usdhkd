from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
import datetime

class UsdhkdRate(Base):
    """
    Modèle pour stocker l'historique du taux de change USD/HKD.
    """
    __tablename__ = "usdhkd_rates"

    id = Column(Integer, primary_key=True, index=True)
    rate = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow, unique=True)

class AggregateBalance(Base):
    """
    Modèle pour stocker l'historique de l'Aggregate Balance.
    """
    __tablename__ = "aggregate_balances"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, nullable=False) # En millions de HKD
    date = Column(DateTime, default=datetime.datetime.utcnow, unique=True)

class HiborRate(Base):
    """
    Modèle pour stocker les taux HIBOR (ex: Overnight, 1 mois, 3 mois).
    """
    __tablename__ = "hibor_rates"

    id = Column(Integer, primary_key=True, index=True)
    period = Column(String, nullable=False) # Ex: "3-month"
    rate = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)