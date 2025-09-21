import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import About from './pages/About';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Projet Shadow USD/HKD</h1>
          <nav className="main-nav">
            <ul>
              <li>
                <NavLink to="/" className={({isActive}) => isActive ? "active" : ""}>
                  Tableau de Bord
                </NavLink>
              </li>
              <li>
                <NavLink to="/about" className={({isActive}) => isActive ? "active" : ""}>
                  À Propos du Projet
                </NavLink>
              </li>
            </ul>
          </nav>
        </header>

        {/* On ajoute une classe ici pour mieux cibler le contenu principal */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;