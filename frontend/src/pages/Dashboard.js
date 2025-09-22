import React, { useState, useEffect } from 'react';
import RateChart from '../components/RateChart';
import AlertBanner from '../components/AlertBanner';
import '../App.css';

const LoadingSpinner = () => (
  <div className="spinner-container">
    <div className="loading-spinner"></div>
  </div>
);

function Dashboard() {
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
        setLoading(true);
        setError(null);

        // ======================= CORRECTION DE L'URL ICI =======================
        const API_BASE_URL = 'https://hadow-usdhkd-api.onrender.com'; // Utilise "hadow"
        // =======================================================================

        const endpoints = [
          `${API_BASE_URL}/api/alerts/status`,
          `${API_BASE_URL}/api/rates/latest`,
          `${API_BASE_URL}/api/rates/history`,
          `${API_BASE_URL}/api/aggregate-balance/latest`,
          `${API_BASE_URL}/api/hibor/latest`
        ];
        
        const requests = endpoints.map(url => fetch(url).then(res => {
          if (!res.ok) {
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
        setError(err.message || "Une erreur est survenue lors de la récupération des données.");
        console.error("Erreur lors de la récupération des données:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 60000);
    return () => clearInterval(interval);
  }, []);

  if (loading && !latestRate) {
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