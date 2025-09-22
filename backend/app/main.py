from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# On importe notre script de récupération de données
from scripts import fetch_data

from . import models, schemas, crud, alerts
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shadow USDHKD API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# ===================== NOUVEL ENDPOINT POUR LE CRON JOB =====================
def run_fetch_script():
    """Fonction wrapper pour appeler toutes les fonctions de fetch."""
    print("Déclenchement du script de récupération des données en arrière-plan...")
    fetch_data.fetch_and_store_rate()
    fetch_data.fetch_and_store_aggregate_balance()
    fetch_data.fetch_and_store_hibor_rate()
    print("Script de récupération des données terminé.")

@app.get("/api/trigger-fetch")
def trigger_fetch(background_tasks: BackgroundTasks):
    """
    Cet endpoint lance le script de récupération des données en tâche de fond.
    C'est cette URL que notre service de cron externe appellera.
    """
    background_tasks.add_task(run_fetch_script)
    return {"message": "La récupération des données a été lancée en arrière-plan."}
# =========================================================================

# ... Le reste des endpoints ne change pas ...
@app.get("/api/alerts/status")
def get_alert_status(db: Session = Depends(get_db)):
    status = alerts.check_trading_conditions(db)
    return status

@app.get("/api/rates/history", response_model=List[schemas.UsdhkdRate])
def read_rate_history(db: Session = Depends(get_db)):
    history = crud.get_rate_history(db)
    return history

@app.get("/api/rates/latest", response_model=schemas.UsdhkdRate)
def read_latest_rate(db: Session = Depends(get_db)):
    latest_rate = crud.get_latest_usdhkd_rate(db)
    if latest_rate is None:
        raise HTTPException(status_code=404, detail="Aucune donnée de taux trouvée")
    return latest_rate

@app.get("/api/aggregate-balance/latest", response_model=schemas.AggregateBalance)
def read_latest_aggregate_balance(db: Session = Depends(get_db)):
    latest_balance = crud.get_latest_aggregate_balance(db)
    if latest_balance is None:
        raise HTTPException(status_code=404, detail="Aucune donnée d'Aggregate Balance trouvée")
    return latest_balance

@app.get("/api/hibor/latest", response_model=schemas.HiborRate)
def read_latest_hibor_rate(db: Session = Depends(get_db)):
    latest_hibor = crud.get_latest_hibor_rate(db)
    if latest_hibor is None:
        raise HTTPException(status_code=404, detail="Aucune donnée HIBOR trouvée")
    return latest_hibor

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Shadow USDHKD."}