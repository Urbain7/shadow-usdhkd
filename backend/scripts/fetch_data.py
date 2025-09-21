import requests
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import UsdhkdRate, AggregateBalance, HiborRate

# URLs des API de la HKMA
URL_USDHKD_RATE = "https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/er-eeri-daily?pagesize=1&sortby=end_of_day&sortorder=desc"
URL_AGGREGATE_BALANCE = "https://api.hkma.gov.hk/public/market-data-and-statistics/daily-monetary-statistics/daily-figures-monetary-base?pagesize=1&sortby=end_of_date&sortorder=desc"
URL_HIBOR_CORRECT = "https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/hk-interbank-ir-daily?segment=hibor.fixing&pagesize=1&sortby=end_of_day&sortorder=desc"

def fetch_and_store_rate():
    print("Tentative de récupération du dernier taux USD/HKD...")
    try:
        response = requests.get(URL_USDHKD_RATE)
        response.raise_for_status()
        data = response.json()
        record = data['result']['records'][0]
        rate_value = record['usd']
        rate_date = datetime.strptime(record['end_of_day'], '%Y-%m-%d').date()
        print(f"Donnée récupérée : Taux = {rate_value} pour la date {rate_date}")
        db = SessionLocal()
        exists = db.query(UsdhkdRate).filter(UsdhkdRate.date == rate_date).first()
        if not exists:
            new_rate = UsdhkdRate(rate=rate_value, date=rate_date)
            db.add(new_rate)
            db.commit()
            print("SUCCÈS : La nouvelle donnée a été enregistrée dans la base.")
        else:
            print("INFO : La donnée pour cette date existe déjà, pas d'ajout nécessaire.")
    except requests.exceptions.RequestException as e:
        print(f"ERREUR : Impossible de contacter l'API de la HKMA. Détails : {e}")
    finally:
        if 'db' in locals():
            db.close()

def fetch_and_store_aggregate_balance():
    print("Tentative de récupération de l'Aggregate Balance...")
    try:
        response = requests.get(URL_AGGREGATE_BALANCE)
        response.raise_for_status()
        data = response.json()
        record = data['result']['records'][0]
        balance_value = record['aggr_balance_bf_disc_win']
        balance_date = datetime.strptime(record['end_of_date'], '%Y-%m-%d').date()
        print(f"Donnée récupérée : Aggregate Balance = {balance_value} M HKD pour la date {balance_date}")
        db = SessionLocal()
        exists = db.query(AggregateBalance).filter(AggregateBalance.date == balance_date).first()
        if not exists:
            new_balance = AggregateBalance(balance=balance_value, date=balance_date)
            db.add(new_balance)
            db.commit()
            print("SUCCÈS : La nouvelle donnée d'Aggregate Balance a été enregistrée.")
        else:
            print("INFO : La donnée d'Aggregate Balance pour cette date existe déjà.")
    except requests.exceptions.RequestException as e:
        print(f"ERREUR lors de la récupération de l'Aggregate Balance: {e}")
    finally:
        if 'db' in locals():
            db.close()

def fetch_and_store_hibor_rate():
    print("Tentative de récupération du taux HIBOR 3 mois...")
    try:
        response = requests.get(URL_HIBOR_CORRECT)
        response.raise_for_status()
        data = response.json()
        
        records = data.get('result', {}).get('records')
        if not records:
            print("INFO: Aucune donnée HIBOR retournée par l'API.")
            return

        latest_record = records[0]
        
        # ======================= CORRECTION FINALE =======================
        # On utilise la clé 'ir_3m' que nous avons découverte.
        hibor_rate_value = latest_record.get('ir_3m')
        # ===============================================================
        
        hibor_date = datetime.strptime(latest_record['end_of_day'], '%Y-%m-%d').date()

        if hibor_rate_value is None:
            # On met à jour le message d'erreur pour être plus précis.
            print(f"INFO: La clé 'ir_3m' n'a pas été trouvée dans la réponse pour la date {hibor_date}.")
            return

        print(f"Donnée retenue : HIBOR 3 mois = {hibor_rate_value}% pour la date {hibor_date}")

        db = SessionLocal()
        exists = db.query(HiborRate).filter(HiborRate.date == hibor_date, HiborRate.period == "3-month").first()

        if not exists:
            new_hibor = HiborRate(rate=hibor_rate_value, date=hibor_date, period="3-month")
            db.add(new_hibor)
            db.commit()
            print("SUCCÈS : Le nouveau taux HIBOR a été enregistré.")
        else:
            print("INFO : Le taux HIBOR 3 mois pour cette date existe déjà.")
            
    except requests.exceptions.RequestException as e:
        print(f"ERREUR lors de la récupération du HIBOR: {e}")
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    fetch_and_store_rate()
    fetch_and_store_aggregate_balance()
    fetch_and_store_hibor_rate()