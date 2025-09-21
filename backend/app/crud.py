from sqlalchemy.orm import Session
from . import models
from datetime import datetime, timedelta

def get_latest_usdhkd_rate(db: Session):
    return db.query(models.UsdhkdRate).order_by(models.UsdhkdRate.date.desc()).first()

def get_rate_history(db: Session, limit: int = 100):
    return db.query(models.UsdhkdRate).order_by(models.UsdhkdRate.date.desc()).limit(limit).all()[::-1]

def get_latest_aggregate_balance(db: Session):
    return db.query(models.AggregateBalance).order_by(models.AggregateBalance.date.desc()).first()

# ===================== NOUVELLE FONCTION =====================
def get_aggregate_balance_history(db: Session, days: int = 7):
    """
    Récupère l'historique de l'Aggregate Balance sur une période donnée en jours.
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    return db.query(models.AggregateBalance).filter(models.AggregateBalance.date >= start_date).order_by(models.AggregateBalance.date.asc()).all()
# =============================================================

def get_latest_hibor_rate(db: Session, period: str = "3-month"):
    return db.query(models.HiborRate).filter(models.HiborRate.period == period).order_by(models.HiborRate.date.desc()).first()