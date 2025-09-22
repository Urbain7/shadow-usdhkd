import React, { useState, useEffect } from 'react';
import RateChart from '../components/RateChart';
import AlertBanner from '../components/AlertBanner';
import '../App.css';

// Un petit composant stylisé pour le chargement
const LoadingSpinner = () => (
  <div className="spinner-container">
    <div className="loading-spinner"></div>
  </div>
);

function Dashboard() {
  // 1. On ajoute les états pour le chargement et les erreurs
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [alertStatus, setAlertStatus] = useState(null);
  const [latestRate, setLatestRate] = useState(null);
  const [history, setHistory] = useState([]);
  const [aggregateBalance, setAggregateBalance] = useState(null);
  const [hiborRate, setHiborRate] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // 2. Juste avant de lancer les requêtes, on s'assure que loading est bien à true
        setLoading(true);
        setError(null); // On réinitialise les erreurs précédentes

       const endpoints = [
  'https://shadow-usdhkd-api.onrender.com/api/alerts/status',
  'https://shadow-usdhkd-api.onrender.com/api/rates/latest',
  'https://shadow-usdhkd-api.onrender.com/api/rates/history',
  'https://shadow-usdhkd-api.onrender.com/api/aggregate-balance/latest',
  'https://shadow-usdhkd-api.onrender.com/api/hibor/latest'
];
        
        // On transforme chaque endpoint en une promesse de fetch
        const requests = endpoints.map(url => fetch(url).then(res => {
          if (!res.ok) { // Si la réponse n'est pas OK (ex: 404, 500)
            throw new Error(`Erreur HTTP ${res.status} pour ${url}`);
          }
          return res.json();
        }));

        const [alertData, latestData, historyData, balanceData, hiborData] = await Promise.all(requests);
        
        setAlertStatus(alertData);
        setLatestRate(latestData);
        setHistory(historyData);
        setAggregateBalance(balanceData);
        setHiborRate(hiborData);

      } catch (err) {
        // 3. Si une erreur se produit, on la stocke dans l'état 'error'
        setError(err.message || "Une erreur est survenue lors de la récupération des données.");
        console.error("Erreur lors de la récupération des données:", err);
      } finally {
        // 4. Que la requête réussisse ou échoue, on arrête le chargement
        setLoading(false);
      }
    };

    fetchData(); // On exécute au chargement
    const interval = setInterval(fetchData, 60000);
    return () => clearInterval(interval);
  }, []);

  // 5. Affichage conditionnel basé sur les nouveaux états
  if (loading && !latestRate) { // On affiche le spinner seulement au premier chargement
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="error-message-container">
        <h2>Erreur de Connexion</h2>
        <p>Impossible de charger les données du marché. Veuillez réessayer plus tard.</p>
        <pre>{error}</pre>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <AlertBanner alertData={alertStatus} />
      <div className="info-cards">
        {/* Les cartes restent les mêmes */}
        <div className="rate-display card">
          <h2>Dernier Taux USD/HKD</h2>
          {latestRate ? (
            <p className="rate-value">{latestRate.rate} <span>(Date: {latestRate.date})</span></p>
          ) : (
            <p>...</p>
          )}
        </div>
        <div className="balance-display card">
          <h2>Aggregate Balance</h2>
          {aggregateBalance ? (
            <p className="balance-value">
              {new Intl.NumberFormat().format(aggregateBalance.balance)}
              <span> M HKD</span>
            </p>
          ) : (
            <p>...</p>
          )}
        </div>
        <div className="hibor-display card">
          <h2>HIBOR 3 Mois</h2>
          {hiborRate ? (
            <p className="hibor-value">
              {hiborRate.rate.toFixed(3)}
              <span> %</span>
            </p>
          ) : (
            <p>...</p>
          )}
        </div>
      </div>
      <div className="chart-container card">
        {history.length > 0 ? (
          <RateChart chartData={history} />
        ) : (
          <p>Données de l'historique non disponibles.</p>
        )}
      </div>
    </div>
  );
}

export default Dashboard;