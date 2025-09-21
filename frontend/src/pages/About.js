import React from 'react';
import './About.css'; // Nous créerons ce fichier CSS juste après

function About() {
  return (
    <div className="about-page">
      <h1>Projet Shadow USD/HKD : Comprendre le Peg</h1>
      
      <div className="about-section">
        <h2>Qu'est-ce que le "Peg" du Dollar de Hong Kong ?</h2>
        <p>
          Le Dollar de Hong Kong (HKD) est "arrimé" (en anglais, "pegged") au Dollar Américain (USD) depuis 1983. Cela signifie que l'Autorité Monétaire de Hong Kong (HKMA) s'engage à maintenir le taux de change dans une fourchette très étroite.
        </p>
      </div>

      <div className="about-section">
        <h2>Les Bandes de Convertibilité : 7.75 - 7.85</h2>
        <p>
          La HKMA garantit que le taux de change USD/HKD ne sortira jamais de la bande comprise entre <strong>7.75</strong> et <strong>7.85</strong>.
        </p>
        <ul>
          <li>
            <strong>Limite Forte (7.75) :</strong> Si le marché essaie de pousser le HKD à s'apprécier (en dessous de 7.75), la HKMA vend des HKD et achète des USD pour affaiblir sa monnaie et la ramener dans la bande.
          </li>
          <li>
            <strong>Limite Faible (7.85) :</strong> Si le marché essaie de pousser le HKD à se déprécier (au-dessus de 7.85), la HKMA achète des HKD et vend des USD de ses réserves pour renforcer sa monnaie.
          </li>
        </ul>
      </div>

      <div className="about-section">
        <h2>Les Indicateurs Clés à Surveiller</h2>
        <p>Ce tableau de bord vous montre les trois indicateurs essentiels pour analyser la santé du peg :</p>
        <dl>
          <dt>Taux de Change USD/HKD</dt>
          <dd>L'indicateur principal. Sa proximité avec les bandes de 7.75 ou 7.85 indique une pression sur le peg et une intervention probable de la HKMA.</dd>

          <dt>Aggregate Balance (Solde Global)</dt>
          <dd>C'est la mesure de la liquidité interbancaire en HKD. Quand la HKMA intervient pour défendre la limite faible (7.85), elle achète des HKD, ce qui réduit l'Aggregate Balance. Une baisse rapide de cet indicateur signale une forte pression sur le peg.</dd>
          
          <dt>HIBOR (Hong Kong Interbank Offered Rate)</dt>
          <dd>Le taux d'intérêt auquel les banques se prêtent des HKD. Quand la liquidité se resserre (l'Aggregate Balance baisse), le HIBOR a tendance à monter. Un HIBOR élevé rend plus coûteuse la vente à découvert du HKD, aidant à défendre le peg.</dd>
        </dl>
      </div>
    </div>
  );
}

export default About;