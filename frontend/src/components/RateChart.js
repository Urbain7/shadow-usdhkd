import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import annotationPlugin from 'chartjs-plugin-annotation';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  annotationPlugin
);

const RateChart = ({ chartData }) => {
  const data = {
    labels: chartData.map(item => item.date),
    datasets: [
      {
        label: 'Taux USD/HKD',
        data: chartData.map(item => item.rate),
        borderColor: '#61dafb',
        backgroundColor: 'rgba(97, 218, 251, 0.5)',
      },
    ],
  };
  
  const options = {
    responsive: true,
    scales: {
      y: {
        min: 7.74,
        max: 7.86,
      }
    },
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Historique du Taux de Change' },
      annotation: {
        annotations: {
          strongSideBand: {
            type: 'line',
            yMin: 7.75,
            yMax: 7.75,
            borderColor: 'lightgreen',
            borderWidth: 2,
            label: {
              // ============ CORRECTION ============
              content: 'Limite Forte (7.75)',
              position: 'end', // On déplace l'étiquette à droite
              backgroundColor: 'rgba(0, 100, 0, 0.7)',
              display: true,
              font: {
                size: 10 // On réduit la taille de la police
              },
              xAdjust: -10, // Léger décalage vers la gauche pour ne pas toucher le bord
              yAdjust: -10, // Léger décalage vers le haut
              // ===================================
            }
          },
          weakSideBand: {
            type: 'line',
            yMin: 7.85,
            yMax: 7.85,
            borderColor: 'lightcoral',
            borderWidth: 2,
            label: {
                // ============ CORRECTION ============
                content: 'Limite Faible (7.85)',
                position: 'end', // On déplace l'étiquette à droite
                backgroundColor: 'rgba(255, 0, 0, 0.6)',
                display: true,
                font: {
                  size: 10 // On réduit la taille de la police
                },
                xAdjust: -10, // Léger décalage vers la gauche
                yAdjust: 10,  // Léger décalage vers le bas
                // ===================================
            }
          }
        }
      }
    }
  }

  return <Line options={options} data={data} />;
};

export default RateChart;