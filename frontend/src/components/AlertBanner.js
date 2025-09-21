import React from 'react';
import './AlertBanner.css'; // Nous créerons ce fichier CSS juste après

const AlertBanner = ({ alertData }) => {
  // Si l'alerte n'est pas active, le composant ne rend rien (il est invisible)
  if (!alertData || !alertData.active) {
    return null;
  }

  // On détermine la classe CSS en fonction du niveau de l'alerte
  // pour pouvoir changer la couleur (ex: 'warning' -> orange, 'critical' -> rouge)
  const bannerClass = `alert-banner ${alertData.level || 'info'}`;

  return (
    <div className={bannerClass}>
      <h3 className="alert-title">{alertData.title}</h3>
      <p className="alert-message">{alertData.message}</p>
    </div>
  );
};

export default AlertBanner;