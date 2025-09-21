from sqlalchemy.orm import Session
from . import crud

# Définition des seuils d'alerte
WEAK_SIDE_THRESHOLD = 7.84
STRONG_SIDE_THRESHOLD = 7.76
# Seuil de baisse de l'AB en pourcentage sur 7 jours
LIQUIDITY_DROP_THRESHOLD_PERCENT = 20.0 

def check_liquidity_conditions(db: Session):
    """
    Analyse la tendance de l'Aggregate Balance sur 7 jours.
    """
    # On récupère l'historique de la dernière semaine
    history = crud.get_aggregate_balance_history(db, days=7)

    # Il nous faut au moins deux points de données pour calculer une tendance
    if not history or len(history) < 2:
        return None # Pas assez de données

    # On prend la plus ancienne et la plus récente valeur de la période
    oldest_balance = history[0].balance
    latest_balance = history[-1].balance

    # On calcule la variation en pourcentage
    if oldest_balance == 0: # Pour éviter la division par zéro
        return None
        
    percentage_change = ((latest_balance - oldest_balance) / oldest_balance) * 100

    # Si la baisse dépasse notre seuil
    if percentage_change < -LIQUIDITY_DROP_THRESHOLD_PERCENT:
        return {
            "active": True,
            "level": "critical", # On peut utiliser un nouveau niveau pour une couleur différente (ex: rouge)
            "title": "ALERTE : Resserrement de Liquidité",
            "message": f"L'Aggregate Balance a chuté de {abs(percentage_change):.2f}% sur les 7 derniers jours. Cela indique une forte pression sur le HKD et des interventions significatives de la HKMA."
        }
        
    return None # Pas d'alerte de liquidité

def check_trading_conditions(db: Session):
    """
    Analyse les dernières données du marché et retourne un statut d'alerte.
    Combine plusieurs types d'alertes.
    """
    # 1. On vérifie d'abord l'alerte la plus critique : la liquidité
    liquidity_alert = check_liquidity_conditions(db)
    if liquidity_alert:
        return liquidity_alert # Si on a une alerte de liquidité, on la retourne en priorité

    # 2. Si pas d'alerte de liquidité, on vérifie le taux de change
    latest_rate_data = crud.get_latest_usdhkd_rate(db)
    if not latest_rate_data:
        return {"active": False, "message": "Données non disponibles."}

    current_rate = latest_rate_data.rate
    if current_rate > WEAK_SIDE_THRESHOLD:
        return {
            "active": True, "level": "warning", "title": "Pression sur la Limite Faible",
            "message": f"Le taux USD/HKD ({current_rate}) a dépassé le seuil d'alerte de {WEAK_SIDE_THRESHOLD}. Intervention de la HKMA probable."
        }

    if current_rate < STRONG_SIDE_THRESHOLD:
        return {
            "active": True, "level": "warning", "title": "Pression sur la Limite Forte",
            "message": f"Le taux USD/HKD ({current_rate}) est sous le seuil d'alerte de {STRONG_SIDE_THRESHOLD}. Intervention de la HKMA probable."
        }

    # 3. Si aucune condition n'est remplie
    return {
        "active": False,
        "message": "Les conditions du marché sont stables."
    }