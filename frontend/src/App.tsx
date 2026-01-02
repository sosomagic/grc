import React from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { CsfBrowser } from './pages/CsfBrowser';
import { Summary } from './components/Summary';
import './App.css';

const Navigation: React.FC = () => {
  const location = useLocation();
  
  return (
    <nav className="nav">
      <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
        CSF Browser
      </Link>
      <Link to="/summary" className={location.pathname === '/summary' ? 'active' : ''}>
        Summary
      </Link>
    </nav>
  );
};

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <header className="header">
          <h1>GRC POC - NIST CSF 2.0 & Privacy Framework</h1>
          <Navigation />
        </header>
        <Routes>
          <Route path="/" element={<CsfBrowser />} />
          <Route path="/summary" element={<Summary />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
